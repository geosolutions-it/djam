import os

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DJAM_DB_NAME"),
        "USER": os.getenv("DJAM_DB_USER"),
        "PASSWORD": os.getenv("DJAM_DB_PASSWORD"),
        "HOST": os.getenv("DJAM_DB_HOST"),
        "PORT": os.getenv("DJAM_DB_PORT"),
        "CONN_TOUT": 900,
    }
}
