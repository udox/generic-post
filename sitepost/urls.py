from django.conf.urls.defaults import *
from django.conf import settings
from sitepost.models import SitePost

urlpatterns = patterns('', 
    (r'^sitepost/(?P<object_id>\d+)/(?P<slug>[\w-]+)?/?$', 'django.views.generic.list_detail.object_detail', {
        'queryset' : SitePost.live.all(),
    }, 'objects'),   
    #(r'^news', include('news.urls', namespace='news')),
)
