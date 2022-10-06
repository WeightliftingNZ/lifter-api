"""Setting file."""

import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

import sentry_sdk
from django.core.management.utils import get_random_secret_key
from faker import Faker
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN_1 = os.getenv("SENTRY_DSN_1", None)
SENTRY_DSN_2 = os.getenv("SENTRY_DSN_2", None)
SENTRY_SAMPLE_RATE = os.getenv("SENTRY_SAMPLE_RATE", "1.0")

if SENTRY_DSN_1 is not None and SENTRY_DSN_2 is not None:
    sentry_sdk.init(
        dsn=f"https://{SENTRY_DSN_1}.ingest.sentry.io/{SENTRY_DSN_2}",
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(SENTRY_SAMPLE_RATE),
        send_default_pii=True,
    )

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
HASHID_FIELD_SALT = os.getenv("HASHID_FIELD_SALT", get_random_secret_key())

SITE_ID = 1

# Fake name

DISABLE_FAKE_NAMES = os.getenv("DISABLE_FAKE_NAMES", "0")
FAKER_SEED = os.getenv("FAKER_SEED", "42")

if not FAKER_SEED.isdigit():
    FAKER_SEED = "42"

Faker.seed(int(FAKER_SEED))
faker = Faker("en_NZ")

# Pagination settings

PAGE_SIZE = 20

# Settings specific to weightlifing

# The youngest an athlete can be
MINIMUM_YEAR_FROM_BIRTH = 5

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Application definition

INSTALLED_APPS = [
    # defaults
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # third-party
    "corsheaders",
    #   dj-rest-auth
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    #   django-rest-framework
    "rest_framework.authtoken",
    "rest_framework",
    #   api documentation
    "drf_spectacular",
    "drf_spectacular_sidecar",
    #   simplejwt
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    #   django extensions
    "django_extensions",
    #   django filters / cripsy forms
    "django_filters",
    "crispy_forms",
    #   whitenoise for development
    "whitenoise.runserver_nostatic",
    #   debug tools
    "debug_toolbar",
    #   auditlog
    "auditlog",
    #   simple history
    "simple_history",
    # custom
    "api",
    "users",
]

AUTH_USER_MODEL = "users.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    )
    # "DEFAULT_THROTTLE_CLASSES": [
    #     "rest_framework.throttling.AnonRateThrottle",
    #     "rest_framework.throttling.UserRateThrottle",
    # ],
    # "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    #
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    #
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "reference_id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    #
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    #
    "JTI_CLAIM": "jti",
    #
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Lifter API",
    "DESCRIPTION": "An API made for lifters",
    "VERSION": "1.0.0",
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

# Database

if os.getenv("DATABASE_URL", "") != "":
    r = urlparse(os.environ.get("DATABASE_URL"))
    # online - for deployment on Digital Ocean
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.path.relpath(r.path, "/"),
            "USER": r.username,
            "PASSWORD": r.password,
            "HOST": r.hostname,
            "PORT": r.port,
            "OPTIONS": {"sslmode": "require"},
        }
    }
else:
    # local
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": 5432,
        }
    }

# Password validation

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


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "NZ"

USE_I18N = True

USE_TZ = True


# Graphic representation of database
GRAPH_MODELS = {
    "all_application": True,
    "group_models": True,
}

# Django Debugging
INTERNAL_IPS = ["127.0.0.1"]


# Auditlog
AUDITLOG_INCLUDE_ALL_MODELS = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MANIFEST_STRICT = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "WARNING",
    },
}

# Producution settings
DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_PRELOAD = True

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_ALL_ORIGINS = False

# Development settings
if os.getenv("DJANGO_DEVELOPMENT", 0) == "1":
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    del SECURE_PROXY_SSL_HEADER
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SRF_COOKIE_SECURE = False

    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = []
