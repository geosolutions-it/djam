import logging

from django.contrib.auth import get_user_model
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class GeoServerUsersView(views.APIView):
    """
    Endpoint returning User list with their permission groups, for Geoserver REST roles service
    """

    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        UserModel = get_user_model()

        user_list = []
        for user in UserModel.objects.all():
            if user.get_group():
                user_list.append(
                    {
                        "username": user.username,
                        "groups": [user.get_group()],
                    }
                )

        return Response({"users": user_list})
