import os

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("DJAM_EMAIL_HOST_USER", "djam@djam.com")
EMAIL_HOST_PASSWORD = os.getenv("DJAM_EMAIL_HOST_PASSWORD", "asdf1234")
