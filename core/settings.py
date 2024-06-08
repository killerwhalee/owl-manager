"""
OwlChem Backend Configuration

This is the settings for OwlChem backend, written in python django.

Configuration which needs to be secured are separated using environment variable.
Define your own environment variable file to configure those settings.

Also OwlChem supports default value for those, which is safe to use.
But please remind that default value is only for development.

Configured by killerwhalee

"""

from pathlib import Path
import os

# Host Name

HOST_NAME = os.environ.get("HOST_NAME", "localhost")


# Base Directory

BASE_DIR = Path(__file__).resolve().parent.parent


# Secret Key for Django

from django.core.management.utils import get_random_secret_key

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = bool(int(os.environ.get("DJANGO_DEBUG", 0)))


# Allowed Hosts

ALLOWED_HOSTS = [f".{HOST_NAME}", "localhost"]


# Trusted CSRF Origins

CSRF_TRUSTED_ORIGINS = [f"https://*.{HOST_NAME}", "http://localhost"]


# CORS Whitelist

CORS_ALLOWED_ORIGINS = [
    f"https://api.{HOST_NAME}",
    f"https://{HOST_NAME}",
    "http://localhost:3000",
]


# Application Definition

INSTALLED_APPS = [
    # System built-in application
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # System vendor applications
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    # User Application
    "user.apps.UserConfig",
    "home.apps.HomeConfig",
    "evaluate.apps.EvaluateConfig",
    "tools.apps.ToolsConfig",
    "database.apps.DatabaseConfig",
]


# Middleware Setting

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Django REST Framework Settings

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        ["rest_framework_simplejwt.authentication.JWTAuthentication"]
        # Use session authentication only in debug mode
        + ["rest_framework.authentication.SessionAuthentication"] * DEBUG
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        ["rest_framework.renderers.JSONRenderer"]
        # Use browsable api only in debug mode
        + ["rest_framework.renderers.BrowsableAPIRenderer"] * DEBUG
    ),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}


# Django JWT Settings

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=2),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer", "bearer"),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}


# Url Configuration

ROOT_URLCONF = "core.urls"


# Templates Setting

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "_templates"],
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


# WSGI Setting

WSGI_APPLICATION = "core.wsgi.application"


# Database Setting
# Default is SQLite3. Override the setting for other option.

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "DJANGO_DATABASE_ENGINE", "django.db.backends.sqlite3"
        ),
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DJANGO_DATABASE_USER", "user"),
        "PASSWORD": os.environ.get("DJANGO_DATABASE_PASSWORD", "password"),
        "HOST": os.environ.get("DJANGO_DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DJANGO_DATABASE_PORT", "5432"),
    }
}


# Customized User Model

AUTH_USER_MODEL = "user.User"


# Password Validation
#
# 1. Password must not be too similar with other user variable.
# 2. Password should be at least 8 characters.
# 3. It is not allowed to use common vulnerable passwords.
# 4. It is not allowed only to use number for password.

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


# Registration
# Redirect to Root for default.

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

DATE_FORMAT = "Y.m.d"

DATETIME_FORMAT = "Y.m.d h:i A"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (For Admin Only)

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "_static"


# User Media

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "_media"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins", "file"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "file": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "_logs/site.log",
            "maxBytes": 1024 * 1024,  # 1 MB
            "backupCount": 256,
            "formatter": "standard",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
}
