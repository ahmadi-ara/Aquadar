from .models import Farm, Zone, Plot,  Supervisor, Waterman
from django.utils import timezone
from rest_framework import serializers
from .models import Run, Outlet, Plot

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ["id", "name", "is_active"]

class ZoneSerializer(serializers.ModelSerializer):
    farm = serializers.PrimaryKeyRelatedField(queryset=Farm.objects.all())

    class Meta:
        model = Zone
        fields = ["id", "name", "farm"]

class PlotSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer(read_only=True)

    class Meta:
        model = Plot
        fields = ["id", "name", "zone"]

class OutletSerializer(serializers.ModelSerializer):
    plot = serializers.PrimaryKeyRelatedField(queryset=Plot.objects.all())

    class Meta:
        model = Outlet
        fields = ["id", "number", "plot"]


class RunSerializer(serializers.ModelSerializer):
    # Accept outlet ID on write
    outlet_id = serializers.PrimaryKeyRelatedField(
        queryset=Outlet.objects.all(),
        source="outlet",
        write_only=True
    )
    # Show outlet details on read
    outlet = OutletSerializer(read_only=True)

    duration_seconds = serializers.SerializerMethodField()
    elapsed_seconds = serializers.SerializerMethodField()

    class Meta:
        model = Run
        fields = [
            "id",
            "outlet_id",       # write-only
            "outlet",          # read-only nested
            "started_at",
            "ended_at",
            "duration_seconds",   # frozen total once ended
            "elapsed_seconds",    # live counter for active runs
            "temperature_c",
            "gps_lat_start",
            "gps_lng_start",
            "gps_lat_end",
            "gps_lng_end",
            "is_anomalous_short",
            "is_anomalous_long",
            "created_by",
        ]
        read_only_fields = [
            "started_at",
            "ended_at",
            "duration_seconds",
            "elapsed_seconds",
            "created_by",
        ]

    def get_duration_seconds(self, obj):
        # If run has ended, return the frozen duration
        return obj.duration_seconds

    def get_elapsed_seconds(self, obj):
        # Only compute live elapsed if still running
        if obj.ended_at:
            return None
        if obj.started_at:
            return int((timezone.now() - obj.started_at).total_seconds())
        return None

    def create(self, validated_data):
        # auto-fill started_at and created_by
        validated_data["started_at"] = timezone.now()
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user
        return super().create(validated_data)



class SupervisorSerializer(serializers.ModelSerializer):
    farms = serializers.PrimaryKeyRelatedField(queryset=Farm.objects.all(), many=True)

    class Meta:
        model = Supervisor
        fields = ["id", "user", "farms", "is_active"]

class WatermanSerializer(serializers.ModelSerializer):
    farm = serializers.PrimaryKeyRelatedField(queryset=Farm.objects.all())

    class Meta:
        model = Waterman
        fields = ["id", "name", "user", "farm", "is_active"]
