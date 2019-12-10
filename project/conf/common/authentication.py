
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # enable email based login
    'apps.identity_provider.auth_backends.AuthenticationEmailBackend'
)
