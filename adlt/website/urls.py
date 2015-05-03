from django.conf import settings
from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('adlt.frontpage.urls')),
    url(r'^accounts/', include('adlt.accounts.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
