from django import template
from django.conf import settings
from django.db.models import Q

from django.contrib.sites.models import Site
from sitepost.models import SitePost

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
    
@register.inclusion_tag('tags/list_posts.html')
#Need to pass through comma delimited str with site ids needed eg "1,2,5"
def list_posts(site_list=None):
    post_limit = settings.GENERAL['POSTS']
    settings_site_list = settings.GENERAL['SITES_DISPLAY']
    
    query_filter = []

    if site_list:
        print" type uni"
        site_list = site_list.split(",")        
        sites_sets = Site.objects.filter(id__in=site_list).order_by('id')
    
    elif settings_site_list:
        print "settings"
        sites_sets = Site.objects.filter(id__in=site_list).order_by('id')     
   
    else:
        print "all"
        sites_sets = Site.objects.all().order_by('id')      
    return {
        'sites': sites_sets,
    }    