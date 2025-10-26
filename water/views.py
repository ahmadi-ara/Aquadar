from django.shortcuts import  render
from django.db.models import Q
from .models import  Outlet, Farm, Zone, Plot
from .serializers import (
    RunSerializer,
    OutletSerializer,
    FarmSerializer,
    ZoneSerializer,
    PlotSerializer,
)
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from datetime import timezone

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Run
from .serializers import RunSerializer
from .utils.weather import fetch_temperature_c
from .utils.anomalies import  check_run_anomalies
from .utils.notifications import  notify_supervisors


# ------------------ Farm / Zone / Plot / Outlet ViewSets ------------------

class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()   # ‚úÖ default queryset
    serializer_class = FarmSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "waterman_profile"):
            return Farm.objects.filter(id=user.waterman_profile.farm_id)
        elif hasattr(user, "supervisor_profile"):
            return user.supervisor_profile.farms.all()
        return Farm.objects.none()

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()   # ‚úÖ default queryset
    serializer_class = ZoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "waterman_profile"):
            return Zone.objects.filter(farm=user.waterman_profile.farm)
        elif hasattr(user, "supervisor_profile"):
            return Zone.objects.filter(farm__in=user.supervisor_profile.farms.all())
        return Zone.objects.none()

class PlotViewSet(viewsets.ModelViewSet):
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Plot.objects.none()

        if hasattr(user, "waterman_profile"):
            qs = Plot.objects.filter(zone__farm=user.waterman_profile.farm)
        elif hasattr(user, "supervisor_profile"):
            qs = Plot.objects.filter(zone__farm__in=user.supervisor_profile.farms.all())

        # üîë Apply zone filter if provided
        zone_id = self.request.query_params.get("zone")
        if zone_id:
            qs = qs.filter(zone_id=zone_id)

        return qs

class OutletViewSet(viewsets.ModelViewSet):
    queryset = Outlet.objects.all()   # ‚úÖ default queryset
    serializer_class = OutletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "waterman_profile"):
            return Outlet.objects.filter(plot__zone__farm=user.waterman_profile.farm)
        elif hasattr(user, "supervisor_profile"):
            return Outlet.objects.filter(plot__zone__farm__in=user.supervisor_profile.farms.all())
        return Outlet.objects.none()

# ------------------ Run ViewSet ------------------


class RunViewSet(viewsets.ModelViewSet):
    """
    API endpoints for starting and stopping irrigation runs.
    """
    serializer_class = RunSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Restrict runs based on user role:
        - Waterman: only runs in their farm
        - Supervisor: only runs in their supervised farms
        """
        user = self.request.user
        qs = Run.objects.select_related(
            "outlet", "outlet__plot", "outlet__plot__zone", "outlet__plot__zone__farm"
        ).order_by("-started_at")

        if hasattr(user, "waterman_profile"):
            return qs.filter(outlet__plot__zone__farm=user.waterman_profile.farm)
        elif hasattr(user, "supervisor_profile"):
            return qs.filter(outlet__plot__zone__farm__in=user.supervisor_profile.farms.all())
        return qs.none()

    def perform_create(self, serializer):
        """
        Called by create() to save a new run.
        Ensures started_at and created_by are set automatically.
        """
        serializer.save(
            started_at=timezone.now(),
            created_by=self.request.user
        )

    @action(detail=True, methods=["post"])
    def stop(self, request, pk=None):
        """
        POST /api/runs/{id}/stop/
        Payload: { gps_lat_end, gps_lng_end, temperature_c? }
        """
        run = get_object_or_404(self.get_queryset(), pk=pk)
        if run.ended_at:
            return Response({"detail": "Run already stopped."}, status=status.HTTP_400_BAD_REQUEST)

        run.ended_at = timezone.now()
        run.gps_lat_end = request.data.get("gps_lat_end")
        run.gps_lng_end = request.data.get("gps_lng_end")


        # Fetch temperature at stop time (or use provided)
        temp = request.data.get("temperature_c")
        if temp is None:
            temp = fetch_temperature_c(run.gps_lat_end, run.gps_lng_end, run.ended_at)
        if temp is not None:
            run.temperature_c = temp

        # Anomaly detection
        issues = check_run_anomalies(run)
        if issues:
            run.is_anomalous_short = issues.get("short", False)
            run.is_anomalous_long = issues.get("long", False)
            run.save()
            notify_supervisors(run, issues)
        else:
            run.save()

        return Response(self.get_serializer(run).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def active(self, request):
        """
        GET /api/runs/active/
        Returns only currently running runs (ended_at is null).
        """
        qs = self.get_queryset().filter(ended_at__isnull=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


# ------------------ HTML Views ------------------

from django.utils import timezone
from django.db.models import Q

def dashboard(request):
    """
    Renders the supervisor dashboard with hierarchical farm/zone/plot/outlet structure.
    """
    farms = Farm.objects.prefetch_related(
        "zones__plots__outlets__runs"
    )

    # Compute anomaly count across all runs
    anomaly_count = Run.objects.filter(
        Q(is_anomalous_short=True) | Q(is_anomalous_long=True)
    ).count()

    now = timezone.now()

    # Annotate runs with elapsed_seconds and is_running
    for farm in farms:
        for zone in farm.zones.all():
            for plot in zone.plots.all():
                for outlet in plot.outlets.all():
                    for run in outlet.runs.all():
                        if run.ended_at:
                            run.is_running = False
                            run.elapsed_seconds = run.duration_seconds or 0
                        else:
                            run.is_running = True
                            run.elapsed_seconds = int((now - run.started_at).total_seconds())

    context = {
        "farms": farms,
        "anomaly_count": anomaly_count,
        "now": now,
    }
    return render(request, "water/dashboard.html", context)


@login_required
def waterman_ui(request):
    farms = Farm.objects.filter(is_active=True)
    context = {"farms": []}
    for farm in farms:
        farm_data = {"farm": farm, "zones": []}
        for zone in farm.zones.all():   # requires related_name="zones" on Zone.farm
            zone_data = {
                "zone": zone,
                "plots": zone.plots.all()   # only plots for this zone
            }
            farm_data["zones"].append(zone_data)
        context["farms"].append(farm_data)
    return render(request, "water/waterman_ui.html", context)

@login_required
def outlet_list(request, plot_id):
    """Second page: list outlets for a given plot"""
    plot = get_object_or_404(Plot, id=plot_id)
    outlets = plot.outlets.all()

    # Check if any outlet in this plot is currently running
    is_any_running = any(
        outlet.runs.filter(ended_at__isnull=True).exists()
        for outlet in outlets
    )

    return render(
        request,
        "water/outlet_list.html",
        {"plot": plot, "outlets": outlets, "is_any_running": is_any_running},
    )


@login_required
def post_login_redirect(request):
    user = request.user
    if hasattr(user, "supervisor_profile"):
        return redirect("dashboard")      # supervisors ‚Üí dashboard
    elif hasattr(user, "waterman_profile"):
        return redirect("waterman_ui")    # watermen ‚Üí waterman UI
    return redirect("dashboard")          # fallback
