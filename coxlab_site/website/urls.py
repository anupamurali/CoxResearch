from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from django.contrib import admin

from models import Video
import views


admin.autodiscover()

video_detail = DetailView.as_view(model=Video)
video_list = ListView.as_view(model=Video)
video_recording = views.RecordView.as_view()

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^video_list$', video_list, name='video_list'),
	url(r'^(?P<pk>[a-z\d]+)/$', video_detail, name='video_detail'),
    url(r'^video_recording', video_recording, name='video_recording'),
    url(r'^(?P<video_id>[a-z\d]+)/post_comment/$', views.post_comment, name='post_comment'),
)
