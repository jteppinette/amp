from django.conf.urls import include, url, static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app import urls

urlpatterns = [
    url('^auth/', include('authentication.urls')),
    url('^', include(urls)),
]

urlpatterns += staticfiles_urlpatterns()
