from django import template
from django.conf import settings
from sitepost.models import *

register = template.Library()   
 
    
@register.inclusion_tag('tags/twitter.html')   
def twitter(obj): 
    tweet_url = obj.get_full_url  
    tweet_title = '%s...' % obj.title[:80]
       
    return {
       'tweet_url': tweet_url, 
       'tweet_title': tweet_title,   
    }


@register.inclusion_tag('tags/twitter_js.html')   
def twitter_js():     
    return ''
        
    
    
