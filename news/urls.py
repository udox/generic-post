from django.conf.urls.defaults import *
from django.conf import settings
from news.models import NewsPost


urlpatterns = patterns('', 
    (r'^news?$', 'django.views.generic.list_detail.object_detail', {
        'queryset' : NewsPost.objects.all(),
    }, 'item'),   
    #(r'^news', include('news.urls', namespace='news')),
)
