from django.contrib import admin
from django.db import models
from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from bbcode.widgets import *
from sitepost.models import *

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

class SiteImageForm(forms.ModelForm):
    image = forms.ImageField(widget=AdminImageWidget)

    class Meta:
        model = SitePostImage

class SitePostImageAdmin(admin.TabularInline):
    model = SitePostImage
    form = SiteImageForm
    extra = 5
    allow_add = True

class SiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', )
    ordering = ('-created_at',)
    content_fields = (
        (None, {'fields': ('title', 'sites', 'status', 'slug', 'created_at')}),
        ('Content', { 'fields' : ('format', 'body', 'teaser')}),
        ('Date & Time', { 'fields' : (('start_date', 'start_time'), ('end_date', 'end_time'))}),
    )
    fieldsets = (
        (None, {'fields': ('title', 'sites','status', 'slug', 'created_at')}),
        ('Content', { 'fields' : ('format', 'body', 'teaser')}),
        ('Date & Time', { 'fields' : (('start_date', 'start_time'), ('end_date', 'end_time'))}),        
    )
    prepopulated_fields = { 'slug' : ('title',) }
   
    def formfield_for_dbfield(self, db_field, **kwargs):
           field = super(SiteAdmin, self).formfield_for_dbfield(db_field, **kwargs)
           if db_field.name == 'body':
               field.widget = AdvancedBBWidget()
           if db_field.name == 'teaser':
               field.widget = SimpleBBWidget()
           return field
       
    inlines = [SitePostImageAdmin,]
    
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super(SiteAdmin, self).save_model(request, obj, form, change)
    
    
admin.site.register(SitePost, SiteAdmin)