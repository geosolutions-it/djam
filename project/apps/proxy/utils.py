import base64
import re
from django.contrib.auth import authenticate
from apps.authorizations.models import AccessRule, Role, Resource


def get_token_from_auth_header(auth_header):
    if re.search("Basic", auth_header, re.IGNORECASE):
        user = basic_auth_authenticate_user(auth_header)
        if user and user.is_active:
            return user
    return None


def basic_auth_authenticate_user(auth_header: str):
    """
    Function performing user authentication based on BasicAuth Authorization header

    :param auth_header: Authorization header of the request
    """
    encoded_credentials = auth_header.split(" ")[
        1
    ]  # Removes "Basic " to isolate credentials
    decoded_credentials = (
        base64.b64decode(encoded_credentials).decode("utf-8").split(":")
    )
    username = decoded_credentials[0]
    password = decoded_credentials[1]
    return perform_authenticate(username, password)


def perform_authenticate(username, password):
    return authenticate(username=username, password=password)

def resource_list(user):
    """
    Function which exports the resources (Proxy services) of a user
    """
    
    if user.is_superuser:
        return Resource.objects.all()
    
    roles = user.get_roles()
    
    # Get the IDs of the user's resources from the AccessRule table
    user_resources = Resource.objects.filter(accessrule__in=AccessRule.objects.filter(role__in=roles)).all()

    return user_resources
