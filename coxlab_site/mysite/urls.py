from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url('website/', include('website.urls', namespace="website")),
    url(r'^admin/', include(admin.site.urls)),
)
