"""
Django settings for hallofjustice project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import dj_database_url
from django.utils.module_loading import import_string
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

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
    'grappelli',  # for better admin
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
    'search',
    'crawler'
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hallofjustice.urls'

WSGI_APPLICATION = 'hallofjustice.wsgi.application'


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
    os.path.join(BASE_DIR, 'hallofjustice/static'),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Templates

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'hallofjustice/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'cjdata.context_processors.main_categories',
    'cjdata.context_processors.state_choices',
)

# Admin

GRAPPELLI_ADMIN_TITLE = 'Hall of Justice'

# Haystack configuration

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'search.backends.PliableSearchEngine',
        'URL': os.getenv('HAYSTACK_URL', 'http://127.0.0.1:9200/'),
        'INDEX_NAME': 'hall_of_justice',
        'EXCLUDED_INDEXES': ['search.search_indexes.CategoryIndex', 'search.search_indexes.TagIndex']
    },
    'autocomplete': {
        'ENGINE': 'search.backends.PliableSearchEngine',
        'URL': os.getenv('HAYSTACK_URL', 'http://127.0.0.1:9200/'),
        'INDEX_NAME': 'hall_of_justice_autocomplete',
        'EXCLUDED_INDEXES': ['search.search_indexes.DatasetIndex']
    }
}
# HAYSTACK_ROUTERS = ['search.routers.CJRouter', 'haystack.routers.DefaultRouter']

ELASTICSEARCH_INDEX_SETTINGS = import_string('search.settings.DATASET_INDEX_SETTINGS')
ELASTICSEARCH_DEFAULT_ANALYZER = 'cjdata_analyzer'
ELASTICSEARCH_MINIMUM_SHOULD_MATCH = '80%'

# See celeryconfig.py for Celery settings


# Debug overrides

if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS += ('debug_toolbar',)
    except ImportError:
        pass
    try:
        import django_pdb
        INSTALLED_APPS = ('django_pdb',) + INSTALLED_APPS
        MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)
    except ImportError:
        pass
