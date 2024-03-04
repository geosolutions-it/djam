import os
from conf.base.base import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATICFILES_LOCATION = "static"

STATIC_HOST = os.environ.get("STATIC_URL", "")
STATIC_URL = f"/{STATICFILES_LOCATION}/"
STATIC_ROOT = os.getenv("DJAM_STATIC_ROOT", os.path.join(BASE_DIR, "static_root"))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
