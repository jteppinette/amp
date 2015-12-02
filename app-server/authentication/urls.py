from django.conf.urls import patterns, url, include

from authentication import views

urlpatterns = patterns('',
    url(r'^login/$', views.auth_login, name="login"),
    url(r'^logout/$', views.auth_logout, name="logout"),
)
