# External
from rest_framework import viewsets

# Local
from .models import Checklist, Item
from .permissions import ChecklistPermissions, ItemPermissions
from .serializers import ChecklistSerializer, ItemSerializer

###########
# ViewSets
###########

class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    permission_classes = (ChecklistPermissions,)

    def get_queryset(self):
        if self.request.user.is_anonymous():
            return Checklist.objects.none()

        return Checklist.objects.filter(user=self.request.user)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (ItemPermissions,)

    def get_queryset(self):
        if self.request.user.is_anonymous():
            return Item.objects.none()

        return Item.objects.filter(checklist__user=self.request.user)
