from django.contrib.auth import get_user_model
from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from apps.user_management.api.filters import UsersFilterSet
from apps.user_management.api.pagination import DefaultPagination
from apps.user_management.api.serializers import UserSerializer


class UserViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    Get users data with proper filtering
    """

    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    filterset_class = UsersFilterSet
    queryset = get_user_model().objects.all()
    pagination_class = DefaultPagination

    def get_renderer_context(self):
        context = super().get_renderer_context()
        context["header"] = [
            "id",
            "username",
            "first_name",
            "last_name",
            "last_login",
            "email",
        ]
        return context
