from django import template

from apps.global_configuration.models import GlobalConfiguration

register = template.Library()


@register.simple_tag
def get_map_url():
    return GlobalConfiguration.load().map_redirect_url

@register.simple_tag
def get_mapstand_url():
    return GlobalConfiguration.load().navbar_redirect_url
