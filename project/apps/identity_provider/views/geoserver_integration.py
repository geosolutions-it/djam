from rest_framework import views, permissions, status
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q

from oidc_provider.views import TokenIntrospectionView
from oidc_provider.lib.endpoints.introspection import TokenIntrospectionEndpoint
from apps.identity_provider.models import Session
from apps.privilege_manager.models import Group


class GeoserverTokenIntrospectionView(TokenIntrospectionView):
    """
    Token introspection providing access_token info shaped according to Geonode for Geoserver integration.

    Usage of this endpoint should be as limited as possible.
    """

    def post(self, request, *args, **kwargs):
        introspection = TokenIntrospectionEndpoint(request)

        try:
            introspection.validate_params()
            dic = {
                'client_id': introspection.params['client_id'],
                'username': introspection.id_token['nickname'],
                'issued_to': introspection.id_token['nickname'],
                'email': introspection.id_token['email'],
                'access_token': introspection.token.access_token,
                'access_type': 'online',
                'active': True,
            }
            return TokenIntrospectionEndpoint.response(dic)
        except Exception:
            return TokenIntrospectionEndpoint.response({'active': False})


class GeoserverAuthKeyIntrospection(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        session_uuid = request.GET.get('authkey')

        try:
            session = Session.objects.get(uuid=session_uuid)
        except (ObjectDoesNotExist, ValidationError):
            return Response({'username': None, 'groups': None}, status=status.HTTP_404_NOT_FOUND)

        user_id = session.get_decoded().get("_auth_user_id", None)
        if user_id is None:
            return Response({'username': None, 'groups': None}, status=status.HTTP_401_UNAUTHORIZED)

        user = get_user_model().objects.get(id=user_id)
        user_groups = Group.objects.filter(Q(users__id=user.id))

        user_groups_names = [user_group.name for user_group in user_groups]

        return Response(
            {
                'username': user.username,
                # 'groups': user_groups_names,
            }
        )



