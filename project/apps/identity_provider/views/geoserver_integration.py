import logging

from rest_framework import views, permissions, status
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from oidc_provider.views import TokenIntrospectionView
from oidc_provider.lib.endpoints.introspection import TokenIntrospectionEndpoint
from apps.identity_provider.models import Session, ApiKey
from apps.privilege_manager.models import Group


logger = logging.getLogger(__name__)


class GeoserverTokenIntrospectionView(TokenIntrospectionView):
    """
    Token introspection providing access_token info shaped according to Geonode for Geoserver integration.

    Usage of this endpoint should be as limited as possible.
    """

    def post(self, request, *args, **kwargs):

        if settings.REQUIRE_SECURE_HTTP_FOR_GEOSERVER_INTROSPECTION and not request.is_secure():
            response = JsonResponse({'error': 'HTTPS required'}, status=status.HTTP_400_BAD_REQUEST)
            response['Cache-Control'] = 'no-store'
            response['Pragma'] = 'no-cache'

            return response

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


class GeoserverIntrospection(views.APIView):

    def user_groups_geoserver_format(self, user_id):
        user_groups = Group.objects.filter(Q(users__id=user_id))

        # Geoserver expects User Groups' names in the form of a string with comma separated values.
        # In order to keep the compatibility with default Geoserver regex, the string is enclosed in a list.
        user_groups_names = [''.join([user_group.name + ',' if i+1 != len(user_groups) else user_group.name for i, user_group in enumerate(user_groups)])]
        return user_groups_names


class GeoserverAuthKeyAndApiKeyIntrospection(GeoserverIntrospection, views.APIView):
    """
    Geoserver integration endpoint, enabling two methods of authorizing requests to Geoserver,
    with in the same format:
        1. AuthKey (session key) - tied to User's login session within Djam
        2. ApiKey (static API key) - tied to User

    AuthKey is relatively short lasting, so exposing an endpoint validating it is rather save.

    ApiKey is static for a long period of time, and has all user's privileges in Geoserver,
    so it's validation should be restricted to only known entities.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):

        if settings.REQUIRE_SECURE_HTTP_FOR_GEOSERVER_INTROSPECTION and not request.is_secure():
            return Response({'username': None, 'groups': None}, status=status.HTTP_400_BAD_REQUEST)

        api_key = request.GET.get('authkey')

        try:
            return self.introspect_session_key(api_key)
        except Exception as e:
            logger.debug(f'AuthKey and ApiKey introspection: AuthKey introspection failed with - {e}')

        try:
            return self.introspect_api_key(api_key)
        except Exception as e:
            logger.debug(f'AuthKey and ApiKey introspection: ApiKey introspection failed with - {e}')

        return Response({'username': None, 'groups': None}, status=status.HTTP_404_NOT_FOUND)

    def introspect_session_key(self, api_key):
        session = Session.objects.get(uuid=api_key)

        user_id = session.get_decoded().get("_auth_user_id", None)
        if user_id is None:
            return Response({'username': None, 'groups': None}, status=status.HTTP_401_UNAUTHORIZED)

        user = get_user_model().objects.get(id=user_id)
        user_groups_names = self.user_groups_geoserver_format(user.id)

        return Response(
            {
                'username': user.username,
                'groups': user_groups_names,
            }
        )

    def introspect_api_key(self, api_key):
        api_key = ApiKey.objects.get(key=api_key)

        if api_key.revoked:
            raise ValidationError(f'API key {api_key.key} is revoked.')

        user = api_key.user
        user_groups_names = self.user_groups_geoserver_format(user.id)

        return Response(
            {
                'username': user.username,
                'groups': user_groups_names,
            }
        )


class GeoserverCredentialsIntrospection(GeoserverIntrospection, views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):

        if settings.REQUIRE_SECURE_HTTP_FOR_GEOSERVER_INTROSPECTION and not request.is_secure():
            return Response({'username': None, 'groups': None}, status=status.HTTP_400_BAD_REQUEST)

        username = request.GET.get('u')
        password = request.GET.get('p')

        try:
            user = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'username': None, 'groups': None})

        if user.check_password(password):
            user_groups_names = self.user_groups_geoserver_format(user.id)

            return Response(
                {
                    'username': user.username,
                    'groups': user_groups_names,
                }
            )
        else:
            return Response({'username': None, 'groups': None})
