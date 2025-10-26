# water/utils/notifications.py
def notify_supervisors(run, issues):
    """
    Placeholder for notifying supervisors about anomalies.
    For now, just print to console.
    Later you can integrate with email, SMS, or push notifications.
    """
    print(f"[ALERT] Run {run.id} anomalies: {issues}")
