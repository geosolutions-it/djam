from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from apps.identity_provider.models import ApiKey
from datetime import datetime, timezone

class DjamTokenAuthentication(TokenAuthentication):
    
    # Set the ApiKey model instead of the defult Token model 
    model = ApiKey

    def authenticate_credentials(self, key):
        # Get the our custom ApiKey model and not the default one
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        except ValidationError:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        
        # Check token.scope is management
        if token.scope != 'management':
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        
        # Check if the token has been expired
        if token.expiry<=datetime.now(timezone.utc):
            raise exceptions.AuthenticationFailed(f"Permissions error: Your token as been expired. Please renew it !")

        return (token.user, token)