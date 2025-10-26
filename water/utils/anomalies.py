# water/utils/anomalies.py
from datetime import timedelta

def check_run_anomalies(run):
    issues = {
        "short": False,
        "long": False,
        "gps": False,
        "temperature": False,
    }

    # Duration
    if run.duration_seconds is not None:
        if run.duration_seconds < 120:  # less than 2 minutes
            issues["short"] = True
        if run.duration_seconds > 1600:  # more than 26 min
            issues["long"] = True

    # GPS
    if not run.gps_lat_start or not run.gps_lat_end:
        issues["gps"] = True
    # elif run.distance_moved() > 100:
    #     issues["gps"] = True

    # Temperature
    if run.temperature_c is not None:
        if run.temperature_c < 0 or run.temperature_c > 50:
            issues["temperature"] = True

    return issues
