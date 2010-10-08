from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings

class SimpleBBWidget(forms.Textarea):
    widget_buttons = u"""
            <button class="default" onclick="return surround('[b]','[/b]', this);"><b>B</b></button>
            <button class="default" onclick="return surround('[i]','[/i]', this);"><i>I</i></button>
            <button class="default" onclick="return insert_link(null, null, null,this);"><u>link</u></button>
    """
    pre_buttons = u"""
        <div style="margin-bottom:10px;" class="cms-toolbar">
    """

    post_buttons = u"""
        </div>
        <textarea %(attrs)s cols="120" rows="15" style="width:100%%;" name=%(name)s>%(value)s</textarea>
    """

    def render(self, name, value, attrs=None):

        if value is None: value = ''
        if attrs:
            attr_out = ' '.join([x+'="'+attrs[x]+'"' for x in attrs])
        widget = (self.pre_buttons + self.widget_buttons + self.post_buttons) \
            % { 'value' : value, 'attrs' : attr_out, 'name' : name, 'margin': 'style="margin-right:10px;"' }
        return mark_safe(widget)

    class Media:
        js = (settings.MEDIA_URL+'js/bbcode.widget.js',)
        css = {
            'all': (settings.MEDIA_URL+'css/post-toolbar.css',)
        }

class AdvancedBBWidget(SimpleBBWidget):   
    def __init__(self):       
        super(AdvancedBBWidget, self).__init__()
        self.widget_buttons += u"""
                <button class="default" onclick="return surround('[h]','[/h]', this);" %(margin)s><b>Heading</b></button>
                <button class="yellow" onclick="return insert_readmore(this);" %(margin)s>Read More</button>
                <button class="green" onclick="return insert_img(null, this);">post image</button>
                <button class="green" onclick="return insert_urlimg(null, null, null, this);" %(margin)s>url image</button>
                <button class="orange" onclick="return insert_youtube(null, this);">youtube</button>
                <button class="orange" onclick="return insert_vimeo(null, this);" %(margin)s>vimeo</button>
                <button class="purple" onclick="return insert_map(null, this);" %(margin)s>map</button>
                <button class="default" onclick="return surround('[pre]','[/pre]', this);">pre</button>
                <button class="red" onclick="return surround('[raw]','[/raw]', this);">raw HTML</button>
        """   