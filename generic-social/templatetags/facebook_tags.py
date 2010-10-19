"""
TODO: 
   setup a conf for the fb vars
   set img url in conf    
"""
from django import template
from django.conf import settings
from sitepost.models import *
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site

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
    image = 'default vans logo image? maybe see if we can add img scr as the more link gallery option?'
    url = obj.get_full_url   
    site_name = Site.objects.get_current().name
    type = 'article'  
    fbadmins = '100000670576512'    
        
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

    
        
    
    
