from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from social.conf import *
from social.exceptions import FacebookParameterException

from sitepost.models import *

register = template.Library()

facebook_exceptions = {}

@register.inclusion_tag('tags/facebook_like_iframe.html')
def facebook_like_iframe(obj):  
    url = obj.get_full_url  
    
    return { 
        'fblike_url': url
    } 
       
    
@register.inclusion_tag('tags/facebook_like_meta.html')
def facebook_like_meta(obj):    
    
    title = obj.title[:150]

    if not FACEBOOK_LIKE['IMAGE']:
        facebook_exceptions['image'] = 'No image url found in conf' 
        #raise FacebookParameterException('facebook image FACEBOOK_LIKE[\'IMAGE\']')                
    
    image = FACEBOOK_LIKE['IMAGE']
    url = obj.get_full_url   
    site_name = Site.objects.get_current().name
    type = 'article'  
   
    if not FACEBOOK_LIKE['FBADMINS']:
        facebook_exceptions['fbadmins'] = 'No fb admin uids found in conf' 
          
    fbadmins = FACEBOOK_LIKE['FBADMINS']

    return {
        'fblike_meta': {   
            'title': title, 
            'type': type,
            'image': image,
            'url': url,
            'site_name' : site_name,                            
            'fbadmins': fbadmins,                            
            }, 
    }
    
# Error messages for missing social.conf parameters will only display in debug = true mode
@register.inclusion_tag('tags/facebook_exceptions.html')
def facebook_except(): 
    if settings.DEBUG and facebook_exceptions:
        facebook_exceptions['errors'] = 'Missing parameterts detected in conf these \
            these are required for facebook like button functionality to work'     
        
        return {
            'fb_errors': {
                'error': facebook_exceptions['errors'],
                'image': facebook_exceptions['image'],
                'fbadmins': facebook_exceptions['fbadmins'], 
            }
            
        }

    
        
    
    
