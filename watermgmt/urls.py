from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from water import urls as water_urls
from water.views import post_login_redirect   # 👈 import the redirect view

urlpatterns = [
    path("admin/", admin.site.urls),

    # API endpoints mounted under /api/
    path("api/", include(water_urls.api_urlpatterns)),

    # Redirect root URL to the dashboard
    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False)),

    # HTML views (dashboard, waterman UI)
    path("", include("water.urls")),

    # Django’s built-in auth (login/logout/password reset)
    path("accounts/", include("django.contrib.auth.urls")),

    # Role-based redirect after login
    path("post-login/", post_login_redirect, name="post_login"),
]
