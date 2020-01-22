import logging

from rest_framework import viewsets, views, permissions
from rest_framework.response import Response

from apps.privilege_manager.models import Group
from apps.privilege_manager.serializers import GroupSerializer

logger = logging.getLogger(__name__)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GeoServerRolesView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        group_names = [group.name for group in Group.objects.all()]
        group_names.append('admin')

        return Response({'groups': group_names})
