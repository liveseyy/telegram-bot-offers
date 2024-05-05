"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import environ
import logging
from pathlib import Path


env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get_value("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.get_value("DEBUG") == "1"

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_bootstrap5',

    'avito_parse',
    'bot',
    'common',
    'web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': env.db(var='DSN__DATABASE'),
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (os.path.join(PROJECT_DIR, "static"),)

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media")
MEDIA_URL = "/media/"
FILE_UPLOAD_PERMISSIONS = 0o777

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


TG_BOT_TOKEN = env.get_value("TG_BOT_TOKEN")

WEB_DOMAIN = env.get_value("WEB_DOMAIN")


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.get_value("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

RABBITMQ = {
    "HOSTS": env.get_value("RABBITMQ_HOSTS"),
    "USER": env.get_value("RABBITMQ_USER"),
    "PASSWORD": env.get_value("RABBITMQ_PASSWORD"),
    "VHOST": env.get_value("RABBITMQ_VHOST"),
}

OFFERS_CAR_WATCHER_FORM_CREATE_URL_PREFIX = "offers_watchers_create_form"
OFFERS_CAR_WATCHER_FORM_EDIT_URL_PREFIX = "offers_watchers_edit_form"

BOOTSTRAP5 = {
    # Enable or disable Bootstrap 5 server side validation classes (separate from the indicator classes above).
    'server_side_validation': False,
}


LOGGING_LEVEL = 'DEBUG' if DEBUG else 'WARNING'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} - {name} - {levelname} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'avito_parse': {
            'level': LOGGING_LEVEL,
            'class': 'logging.FileHandler',
            'filename': "avito_parse.log",
            'formatter': 'verbose',
        },
        'send_offers': {
            'level': LOGGING_LEVEL,
            'class': 'logging.FileHandler',
            'filename': "send_offers.log",
            'formatter': 'verbose',
        },
        'bot': {
            'level': LOGGING_LEVEL,
            'class': 'logging.FileHandler',
            'filename': "bot.log",
            'formatter': 'verbose',
        },
        'sync_watchers_with_offers': {
            'level': LOGGING_LEVEL,
            'class': 'logging.FileHandler',
            'filename': "sync_watchers_with_offers.log",
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'avito_parse': {
            'handlers': ['avito_parse'],
            'level': LOGGING_LEVEL,
            'propagate': True,
        },
        'send_offers': {
            'handlers': ['send_offers'],
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
        'bot': {
            'handlers': ['bot'],
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
        'sync_watchers_with_offers': {
            'handlers': ['sync_watchers_with_offers'],
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
    },
}

BUILD = {"assets_version": "1"}


PARSE_TIMEOUT_SECONDS = 0

TELEGRAM_BOT_DOMAIN = "avito_offer_helper_bot"
