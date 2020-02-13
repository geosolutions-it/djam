import os
from django.conf import settings
from django.core.checks import Error, register


REQUIRED_ENVVAR_CONFIG = [
    'DJAM_SECRET_KEY',

    'DJAM_DB_NAME',
    'DJAM_DB_USER',
    'DJAM_DB_PASSWORD',
    'DJAM_DB_HOST',
    'DJAM_DB_PORT',
    'DJAM_DB_NAME',

    'DJAM_RABBITMQ_HOST',
    'DJAM_RABBITMQ_PORT',

    'DJAM_EMAIL_HOST',
    'DJAM_EMAIL_PORT',
    'DJAM_EMAIL_HOST_USER',
    'DJAM_EMAIL_HOST_PASSWORD',
]


@register()
def environment_check(app_configs, **kwargs):
    errors = []

    for envvar_name in REQUIRED_ENVVAR_CONFIG:
        if os.getenv(envvar_name) is None:
            errors.append(
                Error(
                    f'Environment configuration error: "{envvar_name}" not found in environment variables',
                    hint=f'Please add "{envvar_name}" to your environment variables',
                    obj=settings,
                    id='djam.config.E001',
                )
            )

    return errors
