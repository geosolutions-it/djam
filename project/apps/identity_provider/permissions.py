from rest_framework import permissions
from django.core.exceptions import ValidationError
from apps.identity_provider.models import ApiKey
from datetime import datetime, timezone

class ResourceKeyVerification(permissions.BasePermission):
    """
    Verification checks of the resource key
    """
    message = "Invalid resource key"

    def has_permission(self, request, view):
        
        authkey = request.GET.get("authkey")
        try:
            api_key = ApiKey.objects.filter(key=authkey).first()
        except ValidationError:
            return False
        
        if api_key.revoked:
            return False
        
        # Check if the token has not a resource scope
        elif api_key.scope != 'resource':
            return False

        # Check if the token has been expired
        elif api_key.expiry<=datetime.now(timezone.utc):
            return False
        else:
            return True
    