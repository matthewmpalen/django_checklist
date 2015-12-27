# External
from rest_framework.serializers import HyperlinkedModelSerializer

# Local
from .models import Checklist, Item

class ChecklistSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Checklist

class ItemSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Item
        depth = 1
