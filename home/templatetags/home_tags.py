import datetime
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from home.models import Result, Run

register = template.Library()


@register.simple_tag(name='get_config')
def get_config(section, value, fallback=None):
    return settings.CONFIG.get(section, value, fallback=fallback)


@register.filter(name='get_runs_by_username')
def get_runs_by_username(username):
    user = User.objects.get(username=username)
    return Run.objects.get_runs(user)


@register.filter(name='get_result_wins')
def get_result_wins(user):
    return Result.objects.get_wins(user)


@register.filter(name='fmt_offset')
def fmt_offset(value):
    try:
        return 'Winner' if value == 0 else value
    except Exception:
        return value


@register.filter(name='fmt_seconds')
def fmt_seconds(value):
    try:
        return str(datetime.timedelta(seconds=value))
    except Exception:
        return value
