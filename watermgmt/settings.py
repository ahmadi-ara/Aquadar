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
    "pwa",
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
# STATIC_ROOT = BASE_DIR / "static"

# (optional) extra places to look for static files during development
STATICFILES_DIRS = [BASE_DIR / "static",]


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


# PWA
PWA_CONFIG = {
    "name": "Water Management(Aquadar)",
    "short_name": "Aquadar",
    "theme_color": "#421CFF",
    "background_color": "#5B46C2",
    "display": "standalone",
    "orientation": "portrait",
    "scope": "/",
    "start_url": "/",
    "icons": [
        {
            "src": "/static/icons/windows11/SmallTile.scale-100.png",
            "sizes": "71x71"
        },
        {
            "src": "/static/icons/windows11/SmallTile.scale-125.png",
            "sizes": "89x89"
        },
        {
            "src": "/static/icons/windows11/SmallTile.scale-150.png",
            "sizes": "107x107"
        },
        {
            "src": "/static/icons/windows11/SmallTile.scale-200.png",
            "sizes": "142x142"
        },
        {
            "src": "/static/icons/windows11/SmallTile.scale-400.png",
            "sizes": "284x284"
        },
        {
            "src": "/static/icons/windows11/Square150x150Logo.scale-100.png",
            "sizes": "150x150"
        },
        {
            "src": "/static/icons/windows11/Square150x150Logo.scale-200.png",
            "sizes": "300x300"
        },
        {
            "src": "/static/icons/windows11/Square150x150Logo.scale-400.png",
            "sizes": "600x600"
        },
        {
            "src": "/static/icons/windows11/Wide310x150Logo.scale-125.png",
            "sizes": "388x188"
        },
        {
            "src": "/static/icons/windows11/Wide310x150Logo.scale-150.png",
            "sizes": "465x225"
        },
        {
            "src": "/static/icons/windows11/Wide310x150Logo.scale-200.png",
            "sizes": "620x300"
        },
        {
            "src": "/static/icons/windows11/Wide310x150Logo.scale-400.png",
            "sizes": "1240x600"
        },
        {
            "src": "/static/icons/windows11/LargeTile.scale-100.png",
            "sizes": "310x310"
        },
        {
            "src": "/static/icons/windows11/LargeTile.scale-125.png",
            "sizes": "388x388"
        },
        {
            "src": "/static/icons/windows11/LargeTile.scale-150.png",
            "sizes": "465x465"
        },
        {
            "src": "/static/icons/windows11/LargeTile.scale-200.png",
            "sizes": "620x620"
        },
        {
            "src": "/static/icons/windows11/LargeTile.scale-400.png",
            "sizes": "1240x1240"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.scale-100.png",
            "sizes": "44x44"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.scale-125.png",
            "sizes": "55x55"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.scale-150.png",
            "sizes": "66x66"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.scale-200.png",
            "sizes": "88x88"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.scale-400.png",
            "sizes": "176x176"
        },
        {
            "src": "/static/icons/windows11/StoreLogo.scale-100.png",
            "sizes": "50x50"
        },
        {
            "src": "/static/icons/windows11/StoreLogo.scale-125.png",
            "sizes": "63x63"
        },
        {
            "src": "/static/icons/windows11/StoreLogo.scale-150.png",
            "sizes": "75x75"
        },
        {
            "src": "/static/icons/windows11/StoreLogo.scale-200.png",
            "sizes": "100x100"
        },
        {
            "src": "/static/icons/windows11/StoreLogo.scale-400.png",
            "sizes": "200x200"
        },
        {
            "src": "/static/icons/windows11/SplashScreen.scale-100.png",
            "sizes": "620x300"
        },
        {
            "src": "/static/icons/windows11/SplashScreen.scale-125.png",
            "sizes": "775x375"
        },
        {
            "src": "/static/icons/windows11/SplashScreen.scale-150.png",
            "sizes": "930x450"
        },
        {
            "src": "/static/icons/windows11/SplashScreen.scale-200.png",
            "sizes": "1240x600"
        },
        {
            "src": "/static/icons/windows11/SplashScreen.scale-400.png",
            "sizes": "2480x1200"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-16.png",
            "sizes": "16x16"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-20.png",
            "sizes": "20x20"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-24.png",
            "sizes": "24x24"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-30.png",
            "sizes": "30x30"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-32.png",
            "sizes": "32x32"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-36.png",
            "sizes": "36x36"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-40.png",
            "sizes": "40x40"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-44.png",
            "sizes": "44x44"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-48.png",
            "sizes": "48x48"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-60.png",
            "sizes": "60x60"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-64.png",
            "sizes": "64x64"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-72.png",
            "sizes": "72x72"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.targetsize-80.png",
            "sizes": "80x80"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.altform-lightunplated_targetsize-30.png",
            "sizes": "30x30"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.altform-lightunplated_targetsize-32.png",
            "sizes": "32x32"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.altform-lightunplated_targetsize-36.png",
            "sizes": "36x36"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.altform-lightunplated_targetsize-40.png",
            "sizes": "40x40"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.altform-lightunplated_targetsize-44.png",
            "sizes": "44x44"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.altform-lightunplated_targetsize-48.png",
            "sizes": "48x48"
        },
        {
            "src": "/static/icons/windows11/Square44x44Logo.altform-lightunplated_targetsize-256.png",
            "sizes": "256x256"
        },
        {
            "src": "/static/icons/android/android-launchericon-512-512.png",
            "sizes": "512x512"
        },
        {
            "src": "/static/icons/android/android-launchericon-192-192.png",
            "sizes": "192x192"
        },
        {
            "src": "/static/icons/android/android-launchericon-144-144.png",
            "sizes": "144x144"
        },
        {
            "src": "/static/icons/ios/16.png",
            "sizes": "16x16"
        },
        {
            "src": "/static/icons/ios/20.png",
            "sizes": "20x20"
        },
        {
            "src": "/static/icons/ios/29.png",
            "sizes": "29x29"
        },
        {
            "src": "/static/icons/ios/32.png",
            "sizes": "32x32"
        },
        {
            "src": "/static/icons/ios/40.png",
            "sizes": "40x40"
        },
        {
            "src": "/static/icons/ios/50.png",
            "sizes": "50x50"
        },
        {
            "src": "/static/icons/ios/57.png",
            "sizes": "57x57"
        },
        {
            "src": "/static/icons/ios/58.png",
            "sizes": "58x58"
        },
        {
            "src": "/static/icons/ios/60.png",
            "sizes": "60x60"
        },
        {
            "src": "/static/icons/ios/64.png",
            "sizes": "64x64"
        },
        {
            "src": "/static/icons/ios/72.png",
            "sizes": "72x72"
        },
        {
            "src": "/static/icons/ios/76.png",
            "sizes": "76x76"
        },
        {
            "src": "/static/icons/ios/80.png",
            "sizes": "80x80"
        },
        {
            "src": "/static/icons/ios/87.png",
            "sizes": "87x87"
        },
        {
            "src": "/static/icons/ios/100.png",
            "sizes": "100x100"
        },
        {
            "src": "/static/icons/ios/114.png",
            "sizes": "114x114"
        },
        {
            "src": "/static/icons/ios/120.png",
            "sizes": "120x120"
        },
        {
            "src": "/static/icons/ios/128.png",
            "sizes": "128x128"
        },
        {
            "src": "/static/icons/ios/144.png",
            "sizes": "144x144"
        },
        {
            "src": "/static/icons/ios/152.png",
            "sizes": "152x152"
        },
        {
            "src": "/static/icons/ios/167.png",
            "sizes": "167x167"
        },
        {
            "src": "/static/icons/ios/180.png",
            "sizes": "180x180"
        },
        {
            "src": "/static/icons/ios/192.png",
            "sizes": "192x192"
        },
        {
            "src": "/static/icons/ios/256.png",
            "sizes": "256x256"
        },
        {
            "src": "/static/icons/ios/512.png",
            "sizes": "512x512"
        },
        {
            "src": "/static/icons/ios/1024.png",
            "sizes": "1024x1024"
        }
    ],

    "lang": "fa_IR",
    "dir": "rtl",
    "description": "Water Management",
    "version": "1.0",
    "manifest_version": "1.0",
    "author": "Ali Ahmadi & Fazel Momeni"
}
