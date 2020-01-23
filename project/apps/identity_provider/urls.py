from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt

from .views.oidc_customization import StatelessAuthorizeView, TokenViewWithSessionKey, AuthorizeViewWithSessionKey
from .views.geoserver_integration import GeoserverTokenIntrospectionView, GeoserverAuthKeyIntrospection

urlpatterns = [

    # override authorize endpoint to store CODE within Session data
    re_path(r'^authorize/?$', AuthorizeViewWithSessionKey.as_view(), name='authorize'),
    # override Token endpoint to return response updated for Session Token
    re_path(r'^token/?$', csrf_exempt(TokenViewWithSessionKey.as_view()), name='token'),
    # include oidc_provider url
    path('', include('oidc_provider.urls', namespace='oidc_provider')),

    path('authorize/stateless/', StatelessAuthorizeView.as_view()),
    path('introspect/geoserver/', GeoserverTokenIntrospectionView.as_view()),
    path('authkey/introspect/', GeoserverAuthKeyIntrospection.as_view())
]
