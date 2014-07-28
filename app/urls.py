"""
Define the routing used to find the AMP pages.
"""

from django.conf.urls import patterns, url, include

from app import views

urlpatterns = patterns('',
    # Authentication
    url(r'^login/$', views.auth_login),
    url(r'^logout/$', views.auth_logout),
    
    # General
    url(r'^$', views.home),

    # App
    url(r'^dashboard/$', views.dashboard),

    # Requests
    url(r'^requests/employee/new/$', views.NewEmployeeRequest.as_view(), name='new_employee_request'),
)
