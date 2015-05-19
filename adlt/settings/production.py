# pylint: disable=wildcard-import,unused-wildcard-import

from adlt.settings.base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = ['atviriduomenys.lt', 'www.atviriduomenys.lt', 'ad.sirex.lt', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'atviriduomenys',
        'USER': 'atviriduomenys',
    }
}

LOGGING['root'] = {
    'level': 'WARNING',
    'handlers': ['stdout'],
}

SOCIALACCOUNT_PROVIDERS['persona']['AUDIENCE'] = 'ad.sirex.lt'
