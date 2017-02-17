"""
This module contains all the urls related to the calender api

"""
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

import api
import views
import google

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^index/', views.index, name='views-index'),
	url(r'^dateevents/', api.get_events_on_a_date, name='api-get-events'),
    url(r'^events/(?P<pk>\d+)/$', api.Calender.as_view(),
    										name='api-events-details'),
    url(r'^events/', api.Calender.as_view(), name='api-post-events'),
    url(r'^sync/', api.SyncEvent.as_view(), name='api-sync-events'),
    url(r'^gsignup/', google.google_signup, name='api-google_signup'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
    					document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL,
    					document_root=settings.MEDIA_ROOT)
