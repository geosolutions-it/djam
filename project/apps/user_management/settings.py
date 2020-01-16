AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # enable email based login
    'apps.user_management.auth_backends.AuthenticationEmailBackend'
)

# send an email to staff members when a new user register
IP_USER_REGISTRATION_NOTIFICATION = False
# send an email to staff members when a new user confirms their email
IP_USER_EMAIL_CONFIRMATION_NOTIFICATION = False