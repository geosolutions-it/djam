import re
from oidc_provider.views import AuthorizeView

from oidc_provider.views import TokenIntrospectionView
from oidc_provider.lib.endpoints.introspection import TokenIntrospectionEndpoint


class StatelessAuthorizeView(AuthorizeView):
    """
    Authorize view which prevents sending empty state parameter.

    View prepared for integration with Geoserver, which does not send or check state, yet fails on response validation with empty state.
    """

    def get(self, *args, **kwargs):

        response = super().get(*args, **kwargs)

        if response.has_header('location'):
            # check if state param is empty
            if re.search('&state=$', response._headers['location'][1]) or re.search('&state=&', response._headers['location'][1]):
                # remove empty state from redirect url
                response._headers['location'] = ('Location', response._headers['location'][1].replace('&state=', ''))

        return response


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
