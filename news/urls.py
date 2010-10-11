from django.conf.urls.defaults import *
from django.conf import settings
from news.models import NewsPost

urlpatterns = patterns('', 
    (r'^news/(?P<object_id>\d+)/(?P<slug>[\w-]+)?/?$', 'django.views.generic.list_detail.object_detail', {
        'queryset' : NewsPost.live.all(),
    }, 'objects'),   
    #(r'^news', include('news.urls', namespace='news')),
)
