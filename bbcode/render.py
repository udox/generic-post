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
    
    
