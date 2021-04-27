import os

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = float(os.getenv('RECAPTCHA_REQUIRED_SCORE'))
MAPSTAND_URL = 'http://dev-app.mapstand.com'
MAP_URL = 'http://dev-app.mapstand.com'
