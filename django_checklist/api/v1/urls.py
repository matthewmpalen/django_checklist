# Django
from django.conf.urls import include, url

# Local
from django_checklist.common.urls import router as common_router
from django_checklist.django_auth.urls import router as django_auth_router
from django_checklist.todo.urls import router as todo_router

urlpatterns = [
    url(r'', include(django_auth_router.urls)), 
    url(r'^common/', include(common_router.urls)), 
    url(r'^todo/', include(todo_router.urls))
]
