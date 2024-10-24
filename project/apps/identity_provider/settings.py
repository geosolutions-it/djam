import ast, os
import datetime

# include nickname and email in id_token
OIDC_IDTOKEN_INCLUDE_CLAIMS = True

OPENID_URL_PREFIX = "openid"

IP_ACTIVATION_CODE_EXPIRATION_HOURS = 12
IP_ENABLE_OAUTH2_MANAGEMENT_URLPATTERNS = True


# django-oidc-provider custom scope claims conifg
OIDC_EXTRA_SCOPE_CLAIMS = (
    "apps.identity_provider.oidc_provider_settings.CustomScopeClaims"
)

REQUIRE_SECURE_HTTP_FOR_GEOSERVER_INTROSPECTION = ast.literal_eval(os.getenv("DJAM_REQUIRE_SECURE_HTTP_FOR_GEOSERVER_INTROSPECTION", "True"))

# Default expiration delta for the expiry filed of ApiKey model
APIKEY_EXPIRE = datetime.timedelta(ast.literal_eval(os.getenv("DJAM_APIKEY_EXPIRE_DAYS", "30")))

# Short expiration delta for a short expiration date of an old key (/rotate endpoint)
SHORT_APIKEY_EXPIRE = datetime.timedelta(ast.literal_eval(os.getenv("DJAM_SHORT_APIKEY_EXPIRE_DAYS", "3")))

# Max expiration delta for the expiration date of a resource key
MAX_APIKEY_EXPIRE = datetime.timedelta(ast.literal_eval(os.getenv("DJAM_MAX_APIKEY_EXPIRE_DAYS", "180")))

SHOW_API_KEYS_IN_DASHBOARD = ast.literal_eval(os.getenv("DJAM_SHOW_API_KEYS_IN_DASHBOARD", "False"))