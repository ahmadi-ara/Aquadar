# water/permissions.py
def farms_for_user(user):
    if hasattr(user, 'supervisor_profile') and user.supervisor_profile.is_active:
        return user.supervisor_profile.farms.all()
    if hasattr(user, 'waterman_profile') and user.waterman_profile.is_active:
        return [user.waterman_profile.farm]
    return []
