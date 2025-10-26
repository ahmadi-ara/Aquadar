# water/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Run
from .services.weather import fetch_temperature_c

@receiver(post_save, sender=Run)
def fill_temperature_on_start(sender, instance: Run, created, **kwargs):
    if created and instance.gps_lat_start and instance.gps_lng_start and instance.temperature_c is None:
        try:
            temp = fetch_temperature_c(instance.gps_lat_start, instance.gps_lng_start, instance.started_at)
            instance.temperature_c = temp
            instance.save(update_fields=['temperature_c'])
        except Exception:
            # Leave temp null; a periodic job can retry.
            pass
