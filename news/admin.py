from django.contrib import admin
from django.db import models
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _

from bbcode.widgets import *
from news.models import *


def thumbnail(image_path):
    absolute_url = '/media/'+image_path
    return u'<img src="%s" alt="%s" style="width:250px;" />' % (absolute_url, image_path)

class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            try:            # is image
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                output.append('<a target="_blank" href="%s">%s</a><br />%s <a target="_blank" href="%s">%s</a><br />%s ' % \
                    (file_path, thumbnail(file_name), _('Currently:'), file_path, file_name, _('Change:')))
            except IOError: # not image
                output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' % \
                    (_('Currently:'), file_path, file_name, _('Change:')))
        #print output
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
# end theft - TODO: refactor into widget file - working on shell atm ~jaymz

class NewsImageForm(forms.ModelForm):
    image = forms.ImageField(widget=AdminImageWidget)

    class Meta:
        model = NewsPostImage

class NewsPostImageAdmin(admin.TabularInline):
    model = NewsPostImage
    form = NewsImageForm
    extra = 5
    allow_add = True

class NewsAdmin(admin.ModelAdmin):
    content_fields = (
        (None, {'fields': ('title')}),
        ('Content', { 'fields' : ('format', 'body', 'teaser')}),
    )
   
    def formfield_for_dbfield(self, db_field, **kwargs):
           field = super(NewsAdmin, self).formfield_for_dbfield(db_field, **kwargs)
           if db_field.name == 'body':
               field.widget = AdvancedBBWidget()
           if db_field.name == 'teaser':
               field.widget = SimpleBBWidget()
           return field
       
    inlines = [NewsPostImageAdmin,]
admin.site.register(NewsPost, NewsAdmin)