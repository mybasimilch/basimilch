"""
Django settings for basimilch project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "8cd-j&jo=-#ecd1jjulp_s*7y$n4tad(0d_g)l=6@n^r8fg3rn")

DEBUG = os.environ.get("JUNTAGRICO_DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
    "basimilch-test.herokuapp.com",
    "my.basimil.ch",
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
    "basimilch",
    "juntagrico",
    "juntagrico_custom_sub",
    "juntagrico_list_gen",
    "impersonate",
    "crispy_forms",
]

ROOT_URLCONF = "basimilch.urls"


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("JUNTAGRICO_DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("JUNTAGRICO_DATABASE_NAME", "basimilch.db"),
        "USER": os.environ.get("JUNTAGRICO_DATABASE_USER"),
        "PASSWORD": os.environ.get("JUNTAGRICO_DATABASE_PASSWORD"),
        "HOST": os.environ.get("JUNTAGRICO_DATABASE_HOST"),
        "PORT": os.environ.get("JUNTAGRICO_DATABASE_PORT", False),
    }
}

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

LANGUAGE_CODE = "de"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load  'localhost',
# Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
# the internationalization machinery.
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
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"

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


IMPERSONATE = {
    "REDIRECT_URL": "/my/profile",
}

LOGIN_REDIRECT_URL = "/my/home"

"""
    File & Storage Settings
"""
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

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

STYLE_SHEET = "/static/css/basimilch.css"

FAVICON = "/static/img/favicon_basi.ico"
IMAGES = {
    "status_100": "/static/img/indicators/status_100.png",
    "status_75": "/static/img/indicators/status_75.png",
    "status_50": "/static/img/indicators/status_50.png",
    "status_25": "/static/img/indicators/status_25.png",
    "status_0": "/static/img/indicators/single_empty.png",
    "single_full": "/static/img/indicators/single_full.png",
    "single_empty": "/static/img/indicators/single_empty.png",
    "single_core": "/static/img/indicators/single_full.png",
    "core": "/static/img/indicators/single_full.png",
}

ORGANISATION_BANK_CONNECTION = {
    "PC": "-",
    "IBAN": "CH56 0839 0033 6848 1000 7",
    "BIC": "ABSOCH22XXX",
    "NAME": "Alternative Bank Schweiz AG",
}


INFO_EMAIL = "info@basimil.ch"
SERVER_URL = os.environ.get("SERVER_URL", "www.basimil.ch")
ADMINPORTAL_NAME = "Basimilch"
ADMINPORTAL_SERVER_URL = "my.basimil.ch"
SHARE_PRICE = "300"
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
BYLAWS = "https://basimil.ch/genossenschaft/statuten/"
BUSINESS_REGULATIONS = "https://basimil.ch/genossenschaft/betriebsreglement/"
FAQ_DOC = "https://basimil.ch/faq/"
BUSINESS_YEAR_CANCELATION_MONTH = 9

# SPECIFIC SETTINGS FOR HEROKU
USE_S3 = os.environ.get("USE_S3") == "True"

if USE_S3:
    INSTALLED_APPS.append("django_s3_storage")
    DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_REGION = os.environ.get("AWS_REGION")
    AWS_S3_BUCKET_AUTH = False
    AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
