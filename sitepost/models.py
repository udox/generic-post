import os
from django.db import models
from django.conf import settings
from datetime import datetime, date
from django.utils.safestring import mark_safe
from bbcode.render import RenderBBcode
from sorl.thumbnail.fields import ImageWithThumbnailsField
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from sitepost.managers import LiveManager
from sitepost.fields import SlugNullField
import re  
    
class SitePost(models.Model, RenderBBcode):
    
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
    sites = models.ManyToManyField(Site)
    sites.help_text = 'Choose which site(s) this post will appear on'       
    
    def __unicode__(self):
        return self.title
    
    #soley used for admin to create a many to many list_display field
    def sites_attached(self):
        name = None
        s = self.sites.all()
        for x in s:
            if name:
                name = """%s | %s""" % (name, x.name)
            else:
                name =  """%s """ % (x.name)
        return name        
    
    def images(self):
        return SitePostImage.objects.all().filter(site_post=self)
    
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
        return ('sitepost:objects', [self.pk, self.slug])
    
    @property
    def get_full_url(self):
        domain = Site.objects.get_current().domain
        path = self.get_absolute_url()
        return 'http://%s%s' % (domain, path)
    
    objects = models.Manager()
    live = LiveManager()
    
class SitePostImage(models.Model):
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
    site_post = models.ForeignKey(SitePost, blank=True, null=True)
    
    class Meta:
        ordering = ('order',)