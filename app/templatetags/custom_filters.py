from django import template
import datetime

register = template.Library()

def add_days(obj, days):
    if obj is None:
        return None
    else:
        return obj + datetime.timedelta(days=int(days))

register.filter(add_days)
