from rest_framework import permissions
from apps.identity_provider.models import ApiKey
from datetime import datetime, timezone

class ResourceKeyVerification(permissions.BasePermission):
    """
    Check validation of the Resource key validation
    """
    message = "Invalid resource key"

    def has_permission(self, request, view):
        authkey = request.GET.get("authkey")
        api_key = ApiKey.objects.filter(key=authkey).first()
        
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
    