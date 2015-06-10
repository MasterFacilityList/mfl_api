from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def reset_link(uid, token):
    return settings.PASSWORD_RESET_URL.format(uid=uid, token=token)
