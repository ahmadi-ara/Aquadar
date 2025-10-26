# water/reports.py
from django.db.models import Sum
from django.utils import timezone
from .models import Run

def durations_by_plot(start, end, farms):
    qs = Run.objects.filter(ended_at__isnull=False,
                            started_at__gte=start, ended_at__lte=end,
                            outlet__plot__zone__farm__in=farms) \
                    .values('outlet__plot_id', 'outlet__plot__name', 'outlet__plot__zone__name') \
                    .annotate(total_sec=Sum('duration_seconds')) \
                    .order_by('outlet__plot__zone__name', 'outlet__plot__name')
    return list(qs)

def durations_by_outlet(start, end, farms):
    qs = Run.objects.filter(ended_at__isnull=False,
                            started_at__gte=start, ended_at__lte=end,
                            outlet__plot__zone__farm__in=farms) \
                    .values('outlet_id', 'outlet__number', 'outlet__plot__name') \
                    .annotate(total_sec=Sum('duration_seconds')) \
                    .order_by('outlet__plot__name', 'outlet__number')
    return list(qs)
