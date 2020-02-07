import os
from django.core.exceptions import ImproperlyConfigured

EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.getenv("DJAM_EMAIL_HOST", None)
if EMAIL_HOST is None:
    raise ImproperlyConfigured('Missing "EMAIL_HOST" setting value')

EMAIL_PORT = os.getenv("DJAM_EMAIL_PORT", None)
if EMAIL_PORT is None:
    raise ImproperlyConfigured('Missing "EMAIL_PORT" setting value')

EMAIL_HOST_USER = os.getenv("DJAM_EMAIL_HOST_USER", None)
if EMAIL_HOST_USER is None:
    raise ImproperlyConfigured('Missing "EMAIL_HOST_USER" setting value')

EMAIL_HOST_PASSWORD = os.getenv("DJAM_EMAIL_HOST_PASSWORD", None)
if EMAIL_HOST_PASSWORD is None:
    raise ImproperlyConfigured('Missing "EMAIL_HOST_PASSWORD" setting value')

