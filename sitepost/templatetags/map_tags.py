from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('base/tags/render_google_map.html')
def render_google_map(_input):
    """ Returns a map object rendered out. Requires a list of objects which
    inherit from base.models.Locatable. """
    if type(_input)!=list:
        _input = [_input,]
    return {
        'points' : _input,
        'api_key' : settings.GOOGLE_MAPS['API_KEY'],
        'zoom_level' : settings.GOOGLE_MAPS['ZOOM_LEVEL'],
    }

@register.inclusion_tag('base/tags/render_map_fromaddress.html')
def render_map_fromaddress(locatable):
    """ Renders out an address using the address details for a locatable
    object. Fails silently """
    if hasattr(locatable, 'address'):
        return {
            'address': locatable.address,
        }
    else:
        return {
            'address': None,
        }

