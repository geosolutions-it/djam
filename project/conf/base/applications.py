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

]
