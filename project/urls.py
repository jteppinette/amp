from django.conf.urls import include, url, static
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app import urls

urlpatterns = [
    url('^auth/', include('authentication.urls')),
    url('^', include(urls)),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
