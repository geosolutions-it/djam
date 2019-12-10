import os

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("IAM_DB_NAME", "iam"),
        'USER': os.getenv("IAM_DB_USER", 'iam'),
        'PASSWORD': os.getenv("IAM_DB_PASSWORD", 'iam'),
        'HOST': os.getenv("IAM_DB_HOST", 'localhost'),
        'PORT': os.getenv("IAM_DB_PORT", '5432'),
        'CONN_TOUT': 900,
    }
}
