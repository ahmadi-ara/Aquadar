# water/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    FarmViewSet,
    ZoneViewSet,
    PlotViewSet,
    OutletViewSet,
    RunViewSet,
    dashboard,
    waterman_ui,
    outlet_list,   # 👈 new view for outlets in a plot
)
from django.urls import include

# DRF router for API endpoints
router = DefaultRouter()
router.register(r"farms", FarmViewSet)
router.register(r"zones", ZoneViewSet)
router.register(r"plots", PlotViewSet)
router.register(r"outlets", OutletViewSet)
router.register(r"runs", RunViewSet, basename="run")

# App-level urlpatterns (non-API views)
urlpatterns = [
    # Supervisor dashboard (HTML template)
    path("dashboard/", dashboard, name="dashboard"),

    # Waterman UI (phone-first interface)
    path("waterman/", waterman_ui, name="waterman_ui"),

    # Outlet list page for a given plot
    path("waterman/plot/<int:plot_id>/", outlet_list, name="outlet_list"),
    path("api/", include(router.urls)),
]

# Expose router separately so project-level urls.py can mount it under /api/
api_urlpatterns = router.urls

