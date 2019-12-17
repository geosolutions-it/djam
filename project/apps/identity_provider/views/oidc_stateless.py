import re
from oidc_provider.views import AuthorizeView


class StatelessAuthorizeView(AuthorizeView):
    """
    Authorize view which prevents sending empty state parameter.

    View prepared for integration with Geoserver, which does not send or check state, yet fails on response validation with empty state.
    """

    def get(self, *args, **kwargs):

        response = super().get(*args, **kwargs)

        if response.has_header('location'):
            # check if state param is empty
            if re.search('&state=$', response._headers['location'][1]) or re.search('&state=&', response._headers['location'][1]):
                # remove empty state from redirect url
                response._headers['location'] = ('Location', response._headers['location'][1].replace('&state=', ''))

        return response
