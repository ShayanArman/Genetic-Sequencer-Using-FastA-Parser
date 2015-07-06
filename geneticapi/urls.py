# app specific urls
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^get_genetic_info', 'geneticapi.views.get_genetic_info'),
)