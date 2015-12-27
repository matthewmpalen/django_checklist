# External
from rest_framework import routers

# Local
from .views import TagViewSet

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet)
