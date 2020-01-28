import typing

from django.http import HttpRequest
from rest_framework_api_key.permissions import HasAPIKey, KeyParser


class ConfigurableKeyParser(KeyParser):

    def __init__(self, authorization_header_apikey_template='Api-Key '):
        self.authorization_header_apikey_template = authorization_header_apikey_template

    def get_from_authorization(self, request: HttpRequest) -> typing.Optional[str]:
        authorization = request.META.get("HTTP_AUTHORIZATION")

        if not authorization:
            return None

        try:
            _, key = authorization.split(self.authorization_header_apikey_template)
        except ValueError:
            key = None

        return key


class HasGeoserverFormatApiKey(HasAPIKey):
    """
    Api key validator with Authorization header parser looking for 'Authoriaztion: apiKey xxx(...)xxx'
    """
    key_parser = ConfigurableKeyParser('apiKey ')
