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
    def has_permission(self, request, view):
        validated = super().has_permission(request, view)
        if not validated:
            return False

        if view.action == 'create':
            checklist_url = request.data['checklist']
            tokens = checklist_url.split('/')
            checklist_id = int(tokens[-2])
            checklist = Checklist.objects.get(pk=checklist_id)
            if checklist.user != request.user:
                return False

        return True

    def has_object_permission(self, request, view, obj):
        validated = super().has_object_permission(request, view, obj)
        if not validated:
            return False

        return obj.checklist.user == request.user
