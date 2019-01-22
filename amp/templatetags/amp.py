from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def add_days(dt, days):
    return dt + timedelta(days) if dt else None


@register.filter
def startswith(value, prefix):
    if isinstance(value, str):
        return value.startswith(prefix)
    return False
