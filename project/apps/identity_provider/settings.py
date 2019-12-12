
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # enable email based login
    'apps.identity_provider.auth_backends.AuthenticationEmailBackend'
)

# include nickname and email in id_token
OIDC_IDTOKEN_INCLUDE_CLAIMS = True

OPENID_URL_PREFIX = 'openid'

IP_ACTIVATION_CODE_EXPIRATION_HOURS = 12
IP_ENABLE_OAUTH2_MANAGEMENT_URLPATTERNS = True
