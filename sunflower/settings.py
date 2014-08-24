"""
Django settings for sunflower project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""


SITE_NAME = "Sunflower"


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.realpath(os.path.join(BASE_DIR, os.path.pardir))

if "DJANGO_DEBUG_VAR" in os.environ.keys():
    DJANGO_DEBUG_VAR = int(os.environ.get('DJANGO_DEBUG_VAR', 0 ))
else:
    DJANGO_DEBUG_VAR = 0

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'super_secret'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(DJANGO_DEBUG_VAR)
TEMPLATE_DEBUG = False

TEMPLATE_DIRS = (
    os.path.realpath(os.path.join(ROOT_DIR, "templates")),
)

STATICFILES_DIRS = (
    os.path.realpath(os.path.join(ROOT_DIR, "static")),
)

ALLOWED_HOSTS = [
    "localhost",
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "core"
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sunflower.urls'

WSGI_APPLICATION = 'sunflower.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
from django.conf import settings
TEMPLATE_CONTEXT_PROCESSORS  = settings.TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    "core.context_processors.additional_info",
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.realpath(os.path.join(ROOT_DIR, "media"))
STATIC_ROOT = os.path.realpath(os.path.join(ROOT_DIR, "static_root"))
ADMIN_MEDIA_PREFIX = "/static/admin/"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/login"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211"
    }
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.realpath(os.path.join(ROOT_DIR, "logs/django.log")),
        },

    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,

        },

    },

}
