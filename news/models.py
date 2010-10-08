import os
from django.db import models
from django.conf import settings
from bbcode.templatetags.bbcode import bb2xhtml
from sorl.thumbnail.fields import ImageWithThumbnailsField

from PIL import Image

import re

match_post_images = re.compile(r'(\[\[image-[0-9]+\]\])')
match_readmore = re.compile(r'(\[readmore\])')

class RenderBBcode(object):
    def render_body(self, remove_more=True):
        """
        Parses the body content to convert bbcode & my tags into html. All old posts
        are written in HTML format so we give the option of formatting posts either
        way and returning the appropriate data for output.
        """
        if self.body == '' or self.body is None:
            if self.format == 'bbcode':
                return bb2xhtml(self.teaser)
            else:
                return self.teaser
        if self.format == 'html':
            return self.body
        else:
            images = self.images_mapped()
            body = bb2xhtml(self.body)
            if remove_more:
                body = body.replace('[readmore]', '')
            for index in images:
                if images[index].link:
                    repl = '<a href="%s"><img class="news-inline-image" src="%s" alt="%s image" /></a>' \
                        % (images[index].link, images[index].image.url, self.name)
                else:
                    repl = '<img src="%s" class="news-inline-image" alt="%s image" />' \
                        % (images[index].image.url, self.name)
                body = re.sub(r'(\[\[image-%s\]\])' \
                    % (int(index)+1).__str__(), repl, body)
            return mark_safe(body)        
        
    @property
    def clean_body(self):
        return self.render_body(remove_more=False)
    
    def images_mapped(self):
        """
        This returns the images as a dictionary indexed by postitioning
        """
        try:
            return dict([x for x in enumerate(self.images())])
        except:
            return None
    
   
    
class NewsPost(models.Model, RenderBBcode):
    
    FORMAT_CHOICES = (
        ('html', 'Raw HTML'),
        ('bbcode', 'BBCode (recommended)'),
    )
  
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)   
    teaser = models.TextField(blank=True, null=True)
    format = models.CharField(max_length=6, choices=FORMAT_CHOICES, default='bbcode')
    
    def __unicode__(self):
        return self.title
    
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