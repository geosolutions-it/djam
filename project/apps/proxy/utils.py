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
    
    roles_set = set()
    
    # Get the roles of the user
    user_roles = Role.objects.filter(user=user)
    for role in user_roles:
        roles_set.add(role)
    
    #Get user teams
    teams = user.team.all()
    #Get teams roles
    teams_roles = Role.objects.filter(team__in=teams).all()
    for role in teams_roles:
        roles_set.add(role)
    
    # Get the IDs of the user's resources from the AccessRule table
    user_resources = Resource.objects.filter(accessrule__in=AccessRule.objects.filter(role__in=roles_set)).all()

    return user_resources
