"""
Django settings for careercompass_api project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import dotenv_values

env = dotenv_values('.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "user_app",
    "keyword_app",
    "openai_app",
    "onet_app",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "careercompass_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "careercompass_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "careercompass_db",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Token Authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Specify user model
AUTH_USER_MODEL = "user_app.CCUser"

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
    "http://localhost:5173",
    "http://localhost"
]

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": '%(levelname)s %(message)s',
        },
        "verbose": {
            "format": '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    "handlers": {
        "django_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/log/debug.log",
            "formatter": "verbose",
        },
        "django_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/log/info.log",
            "formatter": "verbose",
        },
        "django_warn": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/log/warn.log",
            "formatter": "verbose",
        },
        "django_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/log/error.log",
            "formatter": "verbose",
        },
        "django_crit": {
            "level": "CRITICAL",
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/log/crit.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django_debug": {
            "handlers": ["django_debug"],
            "level": "DEBUG",
            "propegate": True,
        },
        "django_info": {
            "handlers": ["django_info"],
            "level": "INFO",
            "propegate": True,
        },
        "django_warn": {
            "handlers": ["django_warn"],
            "level": "WARNING",
            "propegate": True,
        },
        "django_error": {
            "handlers": ["django_error"],
            "level": "ERROR",
            "propegate": True,
        },
        "django_crit": {
            "handlers": ["django_crit"],
            "level": "CRITICAL",
            "propegate": True,
        },
    },
}
