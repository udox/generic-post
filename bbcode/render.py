import os
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from sitepost.models import *
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
                        % (images[index].link, images[index].image.url, self.title)
                else:
                    repl = '<img src="%s" class="news-inline-image" alt="%s image" />' \
                        % (images[index].image.url, self.title)
                body = re.sub(r'(\[\[image-%s\]\])' \
                    % (int(index)+1).__str__(), repl, body)
            
            return mark_safe(body)        
        
    @property
    def split_body(self):
        return match_readmore.split(self.clean_body)

    @property
    def wordcount(self):
        """Total words in the post body, *not* the teaser"""
        return len(striptags(self.clean_body).split(' '))

    @property
    def remaining_words(self):
        """ Counts the total words remaining - bit rough, may not match
        exactly but should be pretty close """
        words = self.wordcount
        match_split = self.split_body

        if self.teaser and self.body is None or self.body == '':
            return 0 # if teaser is defined the whole thing remains
        
        if self.teaser and self.body:
            return words

        if len(match_split) == 3:
            count = words - len(striptags(match_split[0]).split(' '))
        else:
            count = words - settings.NEWS['AUTO_TEASER_LENGTH']

        if count <= 0:
            return 0

        return count

    @property
    def clean_body(self):
        return self.render_body(remove_more=False)

    @property
    def actual_teaser(self):
        """ Returns the summary content based on the post. If there is a
        teaser defined that is used otherwise it checks if the post has
        a [[more]] tag and returns the first part of the match. Finally
        it will trim it to a certain word length. """
        if self.teaser:
            if self.format == 'bbcode':
                 print "render bbcode"
                 return bb2xhtml(self.teaser)
            else:
                 return self.teaser            
        else:
            clean_body = self.clean_body
            match_split = self.split_body
            if len(match_split) == 3: # we have 1 [[more]] tag
                return match_split[0]
            else:
                return ' '.join(clean_body.split(' ')[:settings.NEWS['AUTO_TEASER_LENGTH']])