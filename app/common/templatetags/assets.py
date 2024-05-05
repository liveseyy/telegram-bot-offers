from django.conf import settings
from django.template import Library

register = Library()


@register.simple_tag(name="assets")
def assets(path):
    return path + "?" + settings.BUILD["assets_version"]
