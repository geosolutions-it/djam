
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


# django-oidc-provider custom scope claims conifg
OIDC_EXTRA_SCOPE_CLAIMS = 'project.apps.identity_provider.oidc_provider_settings.CustomScopeClaims'


# send an email to staff members when a new user register
IP_USER_REGISTRATION_NOTIFICATION = False
# send an email to staff members when a new user confirms their email
IP_USER_EMAIL_CONFIRMATION_NOTIFICATION = False
