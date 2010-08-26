from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings

class NewsAdminWidget(forms.Textarea):
    def render(self, name, value, attrs=None):

        if value is None: value = ''
        if attrs:
            attr_out = ' '.join([x+'="'+attrs[x]+'"' for x in attrs])
        widget = u"""
        <div style="margin-bottom:10px;" class="cms-toolbar">
            <button class="default" onclick="return surround('[b]','[/b]');"><b>B</b></button>
            <button class="default" onclick="return surround('[i]','[/i]');"><i>I</i></button>
            <button class="default" onclick="return insert_link();"><u>link</u></button>
            <button class="default" onclick="return surround('[h]','[/h]');" %(margin)s><b>Heading</b></button>
            <button class="yellow" onclick="return insert_readmore();" %(margin)s>Read More</button>
            <button class="green" onclick="return insert_img();">post image</button>
            <button class="green" onclick="return insert_urlimg();" %(margin)s>url image</button>
            <button class="orange" onclick="return insert_youtube();">youtube</button>
            <button class="orange" onclick="return insert_vimeo();" %(margin)s>vimeo</button>
            <button class="purple" onclick="return insert_map();" %(margin)s>map</button>
            <button class="default" onclick="return surround('[pre]','[/pre]');">pre</button>
            <button class="red" onclick="return surround('[raw]','[/raw]');">raw HTML</button>
        </div>
        <textarea %(attrs)s cols="120" rows="15" style="width:100%%;" name=%(name)s>%(value)s</textarea>
        """ % { 'value' : value, 'attrs' : attr_out, 'name' : name, 'margin': 'style="margin-right:10px;"' }

        return mark_safe(widget)

    class Media:
        js = (settings.MEDIA_URL+'js/bbcode.widget.js',)
        css = {
            'all': (settings.MEDIA_URL+'css/post-toolbar.css',)
        }

