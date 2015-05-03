import configparser
import pathlib

config = configparser.ConfigParser()
config.read('buildout.cfg')

PROJECT_DIR = pathlib.Path(__file__).parents[2]


# Django base settings
# https://docs.djangoproject.com/en/stable/ref/settings/

DEBUG = False
ROOT_URLCONF = 'adlt.website.urls'
SECRET_KEY = config['settings']['secret_key']
MEDIA_URL = '/media/'
MEDIA_ROOT = str(PROJECT_DIR / 'var/www/media')
STATIC_URL = '/static/'
STATIC_ROOT = str(PROJECT_DIR / 'var/www/static')
LANGUAGE_CODE = 'lt'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = []
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
        }
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'atviriduomenys',
    }
}


# Static assets, see config/assets.cfg
# https://pypi.python.org/pypi/hexagonit.recipe.download

STATICFILES_DIRS = (
    str(PROJECT_DIR / 'parts/jquery'),
    str(PROJECT_DIR / 'parts/bootstrap'),
    str(PROJECT_DIR / 'parts/requirejs'),
    str(PROJECT_DIR / 'parts/typeaheadjs'),
)


# django-ompressor settings
# https://pypi.python.org/pypi/django_compressor

INSTALLED_APPS += ('compressor',)
STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


# django-debug-toolbar settings
# https://django-debug-toolbar.readthedocs.org/

INSTALLED_APPS += (
    'debug_toolbar',
)


# django-extensions
# http://django-extensions.readthedocs.org/

INSTALLED_APPS += (
    'django_extensions',
)


# django-nose
# https://pypi.python.org/pypi/django-nose

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

INSTALLED_APPS += (
    'django_nose',
)


# App settings

INSTALLED_APPS += (
    'adlt.core',
    'adlt.website',
    'adlt.accounts',
    'adlt.frontpage',
    'adlt.populatedb',
)


# django-allauth
# http://django-allauth.readthedocs.org/

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
)

TEMPLATE_CONTEXT_PROCESSORS += [
    'django.template.context_processors.request',
    'allauth.socialaccount.context_processors.socialaccount',
]

INSTALLED_APPS += (
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.persona',
)

SORTED_AUTH_PROVIDERS = (
    'persona',
    'openid.google',
    'openid.yahoo',
)

SOCIALACCOUNT_PROVIDERS = {
    'openid': {
        'SERVERS': [
            dict(id='google', name='Google', openid_url='https://www.google.com/accounts/o8/id'),
            dict(id='yahoo', name='Yahoo', openid_url='http://me.yahoo.com'),
        ],
    },
    'persona': {
        'AUDIENCE': '127.0.0.1',
    },
}
