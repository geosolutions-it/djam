import os

EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("DJAM_EMAIL_HOST")
EMAIL_PORT = os.getenv("DJAM_EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("DJAM_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("DJAM_EMAIL_HOST_PASSWORD")

