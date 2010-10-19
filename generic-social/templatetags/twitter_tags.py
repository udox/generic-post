from django import template
from django.conf import settings
from sitepost.models import *
from django.utils.http import urlquote
from django.contrib.sites.models import Site

register = template.Library()   
 
    
@register.inclusion_tag('tags/twitter.html')   
def twitter(obj): 
    tweet_url = obj.get_full_url  
    tweet_title = '%s... Read more at:' % obj.title[:80]  
       
    return {
       'tweet_url': tweet_url,
       'tweet_title': tweet_title,      
    }

    
    
