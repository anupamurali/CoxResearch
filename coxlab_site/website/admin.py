from django.contrib import admin
from django.contrib.admin import site
from website.models import Video
from website.models import Comment
from website.models import Author


class VideoAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'title', 'caption', 'video', 'tags')
    exclude = ('comment',)

site.register(Video, VideoAdmin)
site.register(Comment)
