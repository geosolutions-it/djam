"""
Django settings for iam project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJAM_SECRET_KEY", 'n_8+y!3-qh!*a#sjyk0=^k8u)r770l%g=91q$%u=@*f*1+sma!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = []

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

AUTH_USER_MODEL = 'identity_provider.User'

SESSION_COOKIE_NAME = 'djam_sessionid'
