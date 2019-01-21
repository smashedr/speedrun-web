import datetime
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(name='get_config')
def get_config(section, value, fallback=None):
    return settings.CONFIG.get(section, value, fallback=fallback)


@register.filter(name='fmt_seconds')
def fmt_seconds(value):
    try:
        return str(datetime.timedelta(seconds=value))
    except Exception:
        return value
