# Django
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)), 
    url(r'^api-auth/', include('rest_framework.urls', 
        namespace='rest_framework')), 
    url(r'^api/v1/', include('django_checklist.api.v1.urls'))
]
