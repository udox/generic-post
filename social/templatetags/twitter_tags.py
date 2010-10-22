from django import template
from django.conf import settings
from django.utils.http import urlquote
from django.contrib.sites.models import Site

from sitepost.models import *

register = template.Library()   
 
    
@register.inclusion_tag('tags/twitter.html')   
def twitter(obj): 
    tweet_url = 'http://vans.com/post/post/123897'#obj.get_full_url  
    tweet_title = '%s... Read more at:' % obj.title[:80]  
       
    return {
       'tweet_url': tweet_url,
       'tweet_title': tweet_title,      
    }

    
    
