from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()


@register.simple_tag(name='get_config')
def get_config(section, value, fallback=None):
    return settings.CONFIG.get(section, value, fallback=fallback)


@register.simple_tag(name='icon_url')
def icon_url(icon):
    return icon if icon.lower().startswith('http') else static(icon)


@register.filter(name='clip_id')
def clip_id(value):
    return value.split('/')[3]
