"""
This module forms the basic urls starting point

"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.google import callback

urlpatterns = patterns('',
    url(r'^api/', include('api.urls')),
    url(r'^oauth2callback/', callback),
    url(r'^admin/', include(admin.site.urls)),
)
