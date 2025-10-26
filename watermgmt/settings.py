"""
Django settings for watermgmt project.
Generated baseline for your water management system.
"""

import os
from pathlib import Path

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = "watermgmt.urls"

# -------------------------------------------------
# Security
# -------------------------------------------------
SECRET_KEY = "replace-this-with-a-strong-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]  # in production, restrict to your domain/IP

# -------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
#---------------------------------------------------
# Applications
# -------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "channels",
    # Your apps
    "water",
]

ROOT_URLCONF = "watermgmt.urls"

# settings.py

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# settings.py

# URL prefix for static files
STATIC_URL = "/static/"

# (optional) where collectstatic will gather files for production
#STATIC_ROOT = BASE_DIR / "staticfiles"

# (optional) extra places to look for static files during development
#STATICFILES_DIRS = [BASE_DIR / "static",]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # <— added here
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # optional: your custom templates folder
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



LANGUAGES = [('en', 'English'), ('fa', 'Persian'),]

USE_TZ = True
TIME_ZONE = "Asia/Tehran"

USE_I18N = True
USE_L10N = True

# -------------------------------------------------
# Authentication redirects
# -------------------------------------------------

# Default login URL (where @login_required sends unauthenticated users)
LOGIN_URL = "/accounts/login/"

# Default redirect after login (if no "next" param is provided)
# We'll point this to a small view that decides based on role
LOGIN_REDIRECT_URL = "/post-login/"
