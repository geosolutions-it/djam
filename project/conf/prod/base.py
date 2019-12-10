import os


SECRET_KEY = os.getenv("IAM_SECRET_KEY")

DEBUG = False
# TODO: edit accordingly when deploying
ALLOWED_HOSTS = ['*']
