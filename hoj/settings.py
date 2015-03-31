"""
Django settings for hoj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import dj_database_url
from django.utils.module_loading import import_string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

TEMPLATE_DEBUG = True if os.getenv('TEMPLATE_DEBUG', 'True') == 'True' else DEBUG


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'haystack',
    'elasticstack',
    'localflavor',

    'cjdata',
)

if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS += ('debug_toolbar',)
    except ImportError:
        pass


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hoj.urls'

WSGI_APPLICATION = 'hoj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {'default': dj_database_url.config()}
# DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'hoj/static'),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Templates

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'hoj/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "cjdata.context_processors.main_categories",
    "cjdata.context_processors.state_choices",
)

# Haystack configuration

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'cjdata.search.backends.SimpleESSearchEngine',
        'URL': os.getenv('HAYSTACK_URL', 'http://127.0.0.1:9200/'),
        'INDEX_NAME': 'hall_of_justice',
        'EXCLUDED_INDEXES': ['cjdata.search_indexes.CategoryIndex', 'cjdata.search_indexes.TagIndex']
    },
    'autocomplete': {
        'ENGINE': 'cjdata.search.backends.SimpleESSearchEngine',
        'URL': os.getenv('HAYSTACK_URL', 'http://127.0.0.1:9200/'),
        'INDEX_NAME': 'hall_of_justice_autocomplete',
        'EXCLUDED_INDEXES': ['cjdata.search_indexes.DatasetIndex']
    }
}
# HAYSTACK_ROUTERS = ['cjdata.search.routers.CJRouter', 'haystack.routers.DefaultRouter']

ELASTICSEARCH_INDEX_SETTINGS = import_string('cjdata.search.settings.DATASET_INDEX_SETTINGS')
ELASTICSEARCH_DEFAULT_ANALYZER = 'cjdata_analyzer'
ELASTICSEARCH_MINIMUM_SHOULD_MATCH = '80%'
