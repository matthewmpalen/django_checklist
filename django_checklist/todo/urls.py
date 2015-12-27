# External
from rest_framework import routers

# Local
from .views import ChecklistViewSet, ItemViewSet

router = routers.SimpleRouter()
router.register(r'checklists', ChecklistViewSet)
router.register(r'items', ItemViewSet)
