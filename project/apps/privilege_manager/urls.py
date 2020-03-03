from django.urls import path, include
from rest_framework import routers

from apps.privilege_manager.views.groups import GroupViewSet, GeoServerRolesView, GeoServerAdminRoleView
from apps.privilege_manager.views.users import GeoServerUsersView


router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('api/privilege/', include(router.urls)),
    path('api/privilege/geoserver/roles', GeoServerRolesView.as_view()),
    path('api/privilege/geoserver/adminRole', GeoServerAdminRoleView.as_view()),
    path('api/privilege/geoserver/users', GeoServerUsersView.as_view()),
]
