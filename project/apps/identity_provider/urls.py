from apps.identity_provider.views.token_generator import ApiKeyManager
from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt

from .views.oidc_customization import (
    StatelessAuthorizeView,
    TokenViewWithSessionKey,
    AuthorizeViewWithSessionKey,
)
from .views.geoserver_integration import (
    GeoserverTokenIntrospectionView,
    GeoserverAuthKeyAndApiKeyIntrospection,
    GeoserverCredentialsIntrospection,
)

urlpatterns = [
    # override authorize endpoint to store CODE within Session data
    re_path(r"^authorize/?$", AuthorizeViewWithSessionKey.as_view(), name="authorize"),
    # override Token endpoint to return response updated for Session Token
    re_path(r"^token/?$", csrf_exempt(TokenViewWithSessionKey.as_view()), name="token"),
    # include oidc_provider url
    path("", include("oidc_provider.urls", namespace="oidc_provider")),
    path(
        "authorize/stateless/",
        StatelessAuthorizeView.as_view(),
        name="stateless_authorize",
    ),
    path(
        "introspect/geoserver/",
        GeoserverTokenIntrospectionView.as_view(),
        name="geoserver_token_introspect",
    ),
    path(
        "authkey/introspect/",
        GeoserverAuthKeyAndApiKeyIntrospection.as_view(),
        name="authkey_introspect",
    ),
    path(
        "credentials/introspect/",
        GeoserverCredentialsIntrospection.as_view(),
        name="user_credentials_introspection",
    ),
    path(
        "api/token/",
        ApiKeyManager.as_view(),
        name="api_key_manager",
    ),
]
