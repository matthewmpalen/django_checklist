# Django
from django.contrib.auth.models import User, Group

# External
from rest_framework import viewsets

# Local
from .permissions import UserPermissions, GroupPermissions
from .serializers import UserSerializer, GroupSerializer

###########
# ViewSets
###########

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (GroupPermissions,)
