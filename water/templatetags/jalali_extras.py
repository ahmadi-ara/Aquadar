import jdatetime
from django import template

register = template.Library()

@register.filter
def to_jalali(value, fmt="%Y/%m/%d %H:%M"):
    """
    Convert a Python datetime/date to Jalali string.
    Usage: {{ mydate|to_jalali:"%Y-%m-%d" }}
    """
    if not value:
        return ""
    if hasattr(value, "date"):  # datetime
        g = value
    else:  # date
        from datetime import datetime
        g = datetime.combine(value, datetime.min.time())

    j = jdatetime.datetime.fromgregorian(datetime=g)
    return j.strftime(fmt)
