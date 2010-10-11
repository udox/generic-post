"""
TODO:
    
"""

import os
from django.db import models
from django.db.models import Q, Manager
from django.conf import settings
from datetime import datetime, date
from django.utils.safestring import mark_safe
from bbcode.templatetags.bbcode import bb2xhtml
from bbcode.render import RenderBBcode
from sorl.thumbnail.fields import ImageWithThumbnailsField
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

import re  


class LiveManager(Manager):
    """ A maanger for switchable objects ordered by descending created date """
    def get_query_set(self):
        return super(LiveManager, self).get_query_set().filter(status=5).order_by('-created_at')

# via http://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
# allows us to have a slug field that can be null but also unique
# discussion on the original problem here: http://code.djangoproject.com/ticket/9039

class SlugNullField(models.SlugField):
    description = "SlugField that stores NULL but returns ''"
    def to_python(self, value):  #this is the value right out of the db, or an instance
       if isinstance(value, models.SlugField): #if an instance, just return the instance
              return value
       if value==None:   #if the db has a NULL (==None in Python)
              return ""  #convert it into the Django-friendly '' string
       else:
              return value #otherwise, return just the value
    def get_db_prep_value(self, value):  #catches value right before sending to db
       if value=="":     #if Django tries to save '' string, send the db None (NULL)
            return None
       else:
            return value #otherwise, just pass the value
    
class NewsPost(models.Model, RenderBBcode):
    
    FORMAT_CHOICES = (
        ('html', 'Raw HTML'),
        ('bbcode', 'BBCode (recommended)'),
    )
    
    STATUS_CHOICES = (
        (0, 'Offline'),
        (3, 'Preview'),
        (5, 'Live'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=5)
    status.help_text = 'Use this to take items off the site without deleting them'
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)   
    teaser = models.TextField(blank=True, null=True)
    slug = SlugNullField(null=True, blank=True, unique=True, max_length=255)
    user = models.ForeignKey(User, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    
    start_date = models.DateField(blank=True, null=True)
    start_date.help_text = 'When the event starts'
    start_time = models.TimeField(blank=True, null=True)
    start_time.help_text = 'All day events can leave this blank'
    end_date = models.DateField(blank=True, null=True)
    end_date.help_text = '1-Day events can leave this'
    end_time = models.TimeField(blank=True, null=True)
    
    format = models.CharField(max_length=6, choices=FORMAT_CHOICES, default='bbcode')
    source_object_pk = models.IntegerField(editable=False, blank=True, null=True )       
    
    def __unicode__(self):
        return self.title
    
    def images(self):
        return NewsPostImage.objects.all().filter(news_post=self)
    
    def images_mapped(self):
        """
        This returns the images as a dictionary indexed by positioning
        """
        try:
            return dict([x for x in enumerate(self.images())])
        except:
            return None        
    
    @models.permalink
    def get_absolute_url(self):
        return ('news:objects', [self.pk, self.slug])
    
    @property
    def get_full_url(self):
        domain = Site.objects.get_current().domain
        path = self.get_absolute_url()
        return 'http://%s%s' % (domain, path)
    
    objects = models.Manager()
    live = LiveManager()
    
class NewsPostImage(models.Model):
    """
    This is a quick and easy way for the site editor to link a number of images to a post.
    They then insert them via bb-code syntax in the news post itself
    """
    image = ImageWithThumbnailsField(
        upload_to='uploads/news/',
        thumbnail={'size' : (675, 300), 'options' : ['crop']},
    )
    link = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    news_post = models.ForeignKey(NewsPost, blank=True, null=True)

    class Meta:
        ordering = ('order',)