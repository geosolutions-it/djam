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

class APIKeyManagementResourceKeyVerification(permissions.BasePermission):
    """
    Permission class for the resource key verification which is used
    in the API key management
    """
    message = "No access permissions or invalid resource key"

    def has_permission(self, request, view):
        
        resource_key = request.data.get('resource_key', None)
        other_user = request.data.get('account_id', None)
        
        # Check if the resource key exists
        try:
            api_key = ApiKey.objects.filter(key=resource_key).first()
            if api_key.scope != 'resource':
                return False
        except ValidationError:
            return False
        except ApiKey.DoesNotExist:
                return False
        
        if request.user.is_superuser:
            # check if the account_id exists and if the user of the resource key and the requested account_id are the same
            if other_user != None and other_user != api_key.user_id:
                return False
            else:
                return True
        
        else:
            # Check if the current user has this API key with a resource scope
            try:
                user_resource_key = ApiKey.objects.filter(user=request.user).filter(scope='resource').get(key=resource_key)
            except ValidationError:
                return False
            except ApiKey.DoesNotExist:
                return False
        
            # Check if received resource key owns on this user
            if resource_key == str(user_resource_key.key):
                return True
            else:
                return False
    