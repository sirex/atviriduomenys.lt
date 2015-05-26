from django.conf import settings


def get_website_url(path=''):
    url = settings.SERVER_PROTOCOL + settings.SERVER_NAME
    return url + ('' if path.startswith('/') else '/') + path
