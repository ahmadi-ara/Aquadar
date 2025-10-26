from django.db import models
from django.contrib.auth.models import User
import jdatetime


class Farm(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=100)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="zones")

    def __str__(self):
        return f"{self.name} ({self.farm.name})"


class Plot(models.Model):
    name = models.CharField(max_length=100)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="plots")

    def __str__(self):
        return f"{self.name} ({self.zone.name})"


class Outlet(models.Model):
    number = models.PositiveIntegerField()
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name="outlets")

    def __str__(self):
        return f"{self.number} ({self.plot.name})"


class Run(models.Model):
    outlet = models.ForeignKey(
        Outlet,
        on_delete=models.CASCADE,
        related_name="runs"   # ✅ gives Outlet.runs reverse relation
    )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)

    temperature_c = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    gps_lat_start = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_lng_start = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_lat_end = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_lng_end = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    is_anomalous_short = models.BooleanField(default=False)
    is_anomalous_long = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def get_started_jalali(self):
        if not self.started_at:
            return ""
        # Convert Gregorian datetime to Jalali datetime
        jdt = jdatetime.datetime.fromgregorian(datetime=self.started_at)
        return jdt.strftime('%Y/%m/%d %H:%M:%S')


    def __str__(self):
        return f"Run {self.id} on {self.outlet}"

    # 🔑 Add computed duration property
    @property
    def duration_seconds(self):
        if self.started_at and self.ended_at:
            return int((self.ended_at - self.started_at).total_seconds())
        return None



class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="supervisor_profile")
    farms = models.ManyToManyField(Farm)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Supervisor {self.user.username}"


class Waterman(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="waterman_profile")
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Waterman {self.name} ({self.farm.name})"
