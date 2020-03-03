import os
from conf.base.base import BASE_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':
            [
                os.path.join(BASE_DIR, 'templates'),
                os.path.join(BASE_DIR, 'apps', 'hubspot_integration', 'templates'),
                os.path.join(BASE_DIR, 'apps', 'user_management', 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
