from datetime import datetime

from django.contrib import admin
from django.db import models
from django import forms

from news.models import *
from base.admin import *
from news.widgets import NewsAdminWidget
from gallery.admin import AdminImageWidget

class NewsImageForm(forms.ModelForm):
    image = forms.ImageField(widget=AdminImageWidget)

    class Meta:
        model = NewsPostImage

class NewsPostImageAdmin(admin.TabularInline):
    model = NewsPostImage
    form = NewsImageForm
    extra = 5

class NewsAdmin(BaseAdmin):
    content_fields = (
        (None, {'fields': ('name', 'slug', 'created_at', 'go_live_date')}),
        ('Content', { 'fields' : ('format', 'body', 'teaser')}),
    )
    fieldsets = content_fields+ TagAdmin.fieldsets \
        + LocationAdmin.fieldsets
    list_filter = ('created_at', 'classname',)
    formfield_overrides = {
        models.TextField: {'widget': NewsAdminWidget}, #TODO: this is applying to /any/ textfield. hmm.
    }
    inlines = [NewsPostImageAdmin,]

class EventNewsAdmin(NewsAdmin):
    fieldsets = BaseAdmin.fieldsets + PostAdmin.fieldsets \
        + DateBracketAdmin.fieldsets + LocationAdmin.fieldsets \
        + TagAdmin.fieldsets

class CategorizedAdmin(NewsAdmin):
    list_filter = ('created_at', 'category',)
    fieldsets = (
        ('Content', { 'fields' : ('body', 'category',) }),
    )
    fieldsets = BaseAdmin.fieldsets + fieldsets

class SkateParkAdmin(NewsAdmin):
    fieldsets = (
        ('Skatepark', { 'fields' : ('skatepark',) }),
    )
    fieldsets = fieldsets + NewsAdmin.fieldsets

class BloggerAdmin(admin.ModelAdmin):
    list_display = ('blog', 'category')

admin.site.register(News, NewsAdmin)
admin.site.register(EventNews, EventNewsAdmin)
admin.site.register(MusicNews, NewsAdmin)
admin.site.register(SkateparkNews, SkateParkAdmin)
admin.site.register(CategorizedNews, CategorizedAdmin)
admin.site.register(NewsBlogger, BloggerAdmin)
