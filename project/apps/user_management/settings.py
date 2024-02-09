AUTHENTICATION_BACKENDS = (
    # enable email based login
    "apps.user_management.auth_backends.AuthenticationEmailBackend",
)

# ---- Registration flow modifiers ----
# Require email confirmation
REGISTRATION_EMAIL_CONFIRMATION = True
# Require approval form staff member before activating a user account
REGISTRATION_MODERATION = False
