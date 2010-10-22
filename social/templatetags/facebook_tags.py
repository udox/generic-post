"""
TODO: 
    find a way to check conf (in views?) before we pull conf in template as 
    raising exceptions in templates show ambiguous messages

"""
from django import template
from django.conf import settings
from sitepost.models import *
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from social.conf import *
from social.exceptions import FacebookParameterException

register = template.Library()


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
        raise FacebookParameterException('facebook image FACEBOOK_LIKE[\'IMAGE\']')                
   
    image = FACEBOOK_LIKE['IMAGE']   
    url = obj.get_full_url   
    site_name = Site.objects.get_current().name
    type = 'article'  
   
    if not FACEBOOK_LIKE['FBADMINS']:
        raise FacebookParameterException('fb admin uids FACEBOOK_LIKE[\'FBADMINS\']')
        
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

    
        
    
    
