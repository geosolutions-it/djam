import os

DEBUG = False
ALLOWED_HOSTS = []
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = float(os.getenv('RECAPTCHA_REQUIRED_SCORE'))
MAPSTAND_URL = 'https://app.mapstand.com'
MAP_URL = 'https://app.mapstand.com'
