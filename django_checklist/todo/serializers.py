# External
from rest_framework.serializers import HyperlinkedModelSerializer

# Local
from .models import Checklist, Item

class ChecklistSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Checklist
        read_only_fields = ('user',)

class ItemSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Item
