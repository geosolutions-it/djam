import os


SECRET_KEY = os.getenv("DJAM_SECRET_KEY")

DEBUG = False
# TODO: edit accordingly when deploying
ALLOWED_HOSTS = ['*']
