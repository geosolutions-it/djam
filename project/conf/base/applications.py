# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oidc_provider',
    'corsheaders',
    'rest_framework',
    'django_dramatiq',
    'apps.identity_provider.apps.IdentityProviderConfig',
    'apps.user_management.apps.UserManagementConfig',
    'apps.privilege_manager.apps.PrivilegeManagerConfig',
    'apps.stripe_djam.apps.StripeDjamConfig',
    'apps.hubspot_integration.apps.HubspotIntegrationConfig',
    # Djam health-checks - should always be last in the INSTALLED_APPS
    'checks.ProjectChecksConfig'
]
