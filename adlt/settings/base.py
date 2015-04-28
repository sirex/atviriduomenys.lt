import configparser
import pathlib

config = configparser.ConfigParser()
config.read('buildout.cfg')

PROJECT_DIR = pathlib.Path(__file__).parents[2]


# Django base settings
# https://docs.djangoproject.com/en/stable/ref/settings/

DEBUG = False
ROOT_URLCONF = 'adlt.settings.urls'
SECRET_KEY = config['settings']['secret_key']
MEDIA_URL = '/media/'
MEDIA_ROOT = str(PROJECT_DIR / 'var/www/media')
STATIC_URL = '/static/'
STATIC_ROOT = str(PROJECT_DIR / 'var/www/static')
LANGUAGE_CODE = 'lt'

INSTALLED_APPS = (
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
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


# App settings

INSTALLED_APPS += (
    'adlt.core',
    'adlt.website',
    'adlt.frontpage',
)


# django-crispy-forms settings
# http://django-crispy-forms.readthedocs.org/

CRISPY_TEMPLATE_PACK = 'bootstrap3'

INSTALLED_APPS += (
    'crispy_forms',
)
