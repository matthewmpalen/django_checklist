# External
from rest_framework import permissions

class UserPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if view.action == 'create' or view.action == 'destroy':
            return False
        elif view.action == 'update' or view.action == 'partial_update':
            return False

        if request.user and request.user.is_superuser:
            return True

        return super().has_permission(request, view)

class GroupPermissions(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if view.action == 'create' or view.action == 'destroy':
            return False
        elif view.action == 'update' or view.action == 'partial_update':
            return False

        if request.user and request.user.is_superuser:
            return True

        return super().has_permission(request, view)
