from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension

class DjamAuthTokenScheme(OpenApiAuthenticationExtension):
    target_class = 'apps.identity_provider.permissions.DjamTokenAuthentication'
    name = 'DjamTokenAuthentication'

    def get_security_definition(self, auto_schema):        
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": _(
                'Authentication: Type your management key with the prefix Token. Example: Token <management key>'
            )
        }