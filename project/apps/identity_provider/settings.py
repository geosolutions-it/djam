# include nickname and email in id_token
OIDC_IDTOKEN_INCLUDE_CLAIMS = True

OPENID_URL_PREFIX = 'openid'

IP_ACTIVATION_CODE_EXPIRATION_HOURS = 12
IP_ENABLE_OAUTH2_MANAGEMENT_URLPATTERNS = True


# django-oidc-provider custom scope claims conifg
OIDC_EXTRA_SCOPE_CLAIMS = 'project.apps.identity_provider.oidc_provider_settings.CustomScopeClaims'

REQUIRE_SECURE_HTTP_FOR_GEOSERVER_INTROSPECTION = True
