# External
from rest_framework import permissions

# Local
from .models import Checklist, Item

class ChecklistPermissions(permissions.DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        validated = super().has_object_permission(request, view, obj)
        if not validated:
            return False

        return obj.user == request.user

class ItemPermissions(permissions.DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        validated = super().has_object_permission(request, view, obj)
        if not validated:
            return False

        return obj.user == request.user
