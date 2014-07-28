"""
Define the routing used to find the AMP pages.
"""

from django.conf.urls import patterns, url, include

from app import views

urlpatterns = patterns('',
    url('$', views.home),
)
