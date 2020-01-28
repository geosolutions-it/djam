import logging

from django.contrib.auth import get_user_model
from rest_framework import views
from rest_framework.response import Response
from project.api_key import HasGeoserverFormatApiKey


logger = logging.getLogger(__name__)


class GeoServerUsersView(views.APIView):
    """
    Endpoint returning User list with their permission groups, for Geoserver REST roles service
    """
    permission_classes = [HasGeoserverFormatApiKey]

    def get(self, request, format=None):
        UserModel = get_user_model()

        user_list = []
        for user in UserModel.objects.all():
            user_list.append({'username': user.username, 'groups': [group.name for group in user.group_set.all()]})

        return Response({'users': user_list})
