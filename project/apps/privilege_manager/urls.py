from django.urls import path, include
from rest_framework import routers

from apps.privilege_manager.views.groups import GroupViewSet, GeoServerRolesView


router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('api/privilege/', include(router.urls)),
    path('api/privilege/geoserver/roles', GeoServerRolesView.as_view())
]
