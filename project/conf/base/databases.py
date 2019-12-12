import os

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DJAM_DB_NAME", "djam"),
        'USER': os.getenv("DJAM_DB_USER", 'djam'),
        'PASSWORD': os.getenv("DJAM_DB_PASSWORD", 'djam'),
        'HOST': os.getenv("DJAM_DB_HOST", 'localhost'),
        'PORT': os.getenv("DJAM_DB_PORT", '5432'),
        'CONN_TOUT': 900,
    }
}
