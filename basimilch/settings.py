"""
Django settings for basimilch project.
"""

import os

import dj_database_url
from juntagrico.util import pdf

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "8cd-j&jo=-#ecd1jjulp_s*7y$n4tad(0d_g)l=6@n^r8fg3rn")

DEBUG = os.environ.get("JUNTAGRICO_DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
    "basimilch-test.herokuapp.com" "my.basimil.ch",
    "basimilch.juntagrico.science",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "juntagrico",
    "juntagrico_custom_sub",
    "impersonate",
    "crispy_forms",
    "basimilch",
]

ROOT_URLCONF = "basimilch.urls"


DATABASES = {}
DATABASES["default"] = dj_database_url.config(
    default="sqlite:///yourdatabasename.db", ssl_require=not (DEBUG), conn_max_age=600
)

# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('JUNTAGRICO_DATABASE_ENGINE','django.db.backends.sqlite3'),
#         'NAME': os.environ.get('JUNTAGRICO_DATABASE_NAME','basimilch.db'),
#         'USER': os.environ.get('JUNTAGRICO_DATABASE_USER'), #''junatagrico', # The following settings are not used with sqlite3:
#         'PASSWORD': os.environ.get('JUNTAGRICO_DATABASE_PASSWORD'), #''junatagrico',
#         'HOST': os.environ.get('JUNTAGRICO_DATABASE_HOST'), #'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#         'PORT': os.environ.get('JUNTAGRICO_DATABASE_PORT', False), #''', # Set to empty string for default.
#     }
# }

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader"],
            "debug": True,
        },
    },
]

WSGI_APPLICATION = "basimilch.wsgi.application"

USE_TZ = True

TIME_ZONE = "Europe/Zurich"

LANGUAGE_CODE = "de-CH"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

DATE_INPUT_FORMATS = [
    "%d.%m.%Y",
]

AUTHENTICATION_BACKENDS = ("juntagrico.util.auth.AuthenticateWithEmail", "django.contrib.auth.backends.ModelBackend")


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
]
SECURE_SSL_REDIRECT = not (DEBUG)

EMAIL_HOST = os.environ.get("JUNTAGRICO_EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("JUNTAGRICO_EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("JUNTAGRICO_EMAIL_PASSWORD")
EMAIL_PORT = int(os.environ.get("JUNTAGRICO_EMAIL_PORT", "25"))
EMAIL_USE_TLS = os.environ.get("JUNTAGRICO_EMAIL_TLS", "False") == "True"
EMAIL_USE_SSL = os.environ.get("JUNTAGRICO_EMAIL_SSL", "False") == "True"

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

WHITELIST_EMAILS = []

if os.environ.get("WHITELIST_EMAILS"):
    WHITELIST_EMAILS += os.environ.get("WHITELIST_EMAILS").split(";")


STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

IMPERSONATE = {
    "REDIRECT_URL": "/my/profile",
}

LOGIN_REDIRECT_URL = "/my/home"

"""
    File & Storage Settings
"""
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

MEDIA_ROOT = "media"

"""
     Crispy Settings
"""
CRISPY_TEMPLATE_PACK = "bootstrap4"

"""
     juntagrico Settings
"""
ORGANISATION_NAME = "Basimilch"
ORGANISATION_LONG_NAME = "Basimilch"
ORGANISATION_ADDRESS = {
    "name": "Basimilch",
    "street": "Alte Kindhauserstrasse",
    "number": "3",
    "zip": "8953",
    "city": "Dietikon ZH",
}
ORGANISATION_BANK_CONNECTION = {"PC": "11", "IBAN": "11", "BIC": "11", "NAME": "ZKB", "ESR": ""}
INFO_EMAIL = "info@basimil.ch"
SERVER_URL = os.environ.get("SERVER_URL", "www.basimil.ch")
ADMINPORTAL_NAME = "Basimilch"
ADMINPORTAL_SERVER_URL = "my.basimil.ch"
SHARE_PRICE = "300"
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
