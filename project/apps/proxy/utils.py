import base64
import re
from django.contrib.auth import authenticate


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
