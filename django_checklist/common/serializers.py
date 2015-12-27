# External
from rest_framework.serializers import HyperlinkedModelSerializer

# Local
from .models import Tag

class TagSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Tag
