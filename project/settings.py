import os
from split_settings.tools import optional, include


PROJECT_ENVIRONMENT = os.getenv("DJAM_PROJECT_ENVIRONMENT", "prod")
include(
    "conf/base/*.py", optional(f"conf/{PROJECT_ENVIRONMENT}/*.py"),
)
LOGIN_URL = os.getenv("LOGIN_URL", f"{SITEURL}accounts/login/")
LOGOUT_URL = os.getenv("LOGOUT_URL", f"{SITEURL}accounts/logout/")

ACCOUNT_LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", SITEURL)
ACCOUNT_LOGOUT_REDIRECT_URL = os.getenv("LOGOUT_REDIRECT_URL", SITEURL)
