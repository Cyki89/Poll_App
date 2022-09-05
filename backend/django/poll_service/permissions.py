from rest_framework import permissions

ADMINS_GROUP = 'Admins'

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.groups.filter(name=ADMINS_GROUP)