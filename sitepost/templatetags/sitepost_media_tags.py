from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('tags/googlemaps_script.html')
def render_gmaps_media():
    GMAPS_KEY = settings.GOOGLE_MAPS['API_KEY']    
    if not GMAPS_KEY or GMAPS_KEY == '':
        GMAPS_KEY = None       
    return {
        'GMAPS_KEY' : GMAPS_KEY,
        'MEDIA_URL' : settings.MEDIA_URL       
    }