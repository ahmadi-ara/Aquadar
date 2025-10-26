# water/analytics.py
from django.db.models import Avg
from .models import Run

def flag_anomalies(plot, threshold=0.5):
    # Example: flag runs < 50% or > 200% of plot’s average duration
    avg = Run.objects.filter(outlet__plot=plot, ended_at__isnull=False).aggregate(Avg('duration_seconds'))['duration_seconds__avg'] or 0
    low = int(avg * threshold)
    high = int(avg * (2 / threshold)) if threshold else None
    qs = Run.objects.filter(outlet__plot=plot, ended_at__isnull=False)
    for r in qs:
        r.is_anomalous_short = (avg and r.duration_seconds < low)
        r.is_anomalous_long = (avg and high and r.duration_seconds > high)
    Run.objects.bulk_update(qs, ['is_anomalous_short', 'is_anomalous_long'])
