# water/api.py (simplified DRF views)
from rest_framework import viewsets, permissions, status
import logging

logger = logging.getLogger(__name__)

class FarmScopedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        wm = getattr(request.user, 'waterman_profile', None)
        return wm and wm.is_active

def user_farm(request):
    return request.user.waterman_profile.farm
