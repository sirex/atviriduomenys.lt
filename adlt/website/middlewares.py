from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class WebsiteURLCheckMiddleware(object):
    def process_request(self, request):
        request_url = request.build_absolute_uri('/')
        if settings.WEBSITE_URL != request_url:
            raise ImproperlyConfigured("settings.WEBSITE_URL is set to '%s', but '%s' is received." % (
                settings.WEBSITE_URL, request_url
            ))
