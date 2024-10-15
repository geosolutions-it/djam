from urllib.parse import urlparse, parse_qs, urlencode
from django.http import Http404, HttpResponse, HttpResponseForbidden
from apps.authorizations.models import AccessRule
from revproxy.views import ProxyView
from django.contrib.auth import get_user_model

from apps.proxy.utils import get_token_from_auth_header
from apps.identity_provider.views.geoserver_integration import (
    GeoserverAuthKeyAndApiKeyIntrospection,
)

FORBIDDEN_MESSAGE_403 = "The user does not have enough permissions to see the page"


def proxy_view(request, request_path):
    """
    Will prox the request to a service defined in the admin
    only the users/team with right access can see the proxed response
    """

    user = request.user
    # check if an basic auth or djam token is provided we can authorize it
    auth_header = request.META.get("HTTP_AUTHORIZATION", None)
    if auth_header:
        # getting user object from the header
        user = get_token_from_auth_header(auth_header)
        if not user:
            return HttpResponseForbidden(FORBIDDEN_MESSAGE_403)
    # checking the djam auth token in the url
    elif "authkey" in request.GET and (
        request.user is None or not request.user.is_authenticated
    ):
        # if the introspect is not found, an error is raised
        response = GeoserverAuthKeyAndApiKeyIntrospection().get(request)
        if response.status_code != 200:
            return HttpResponseForbidden(FORBIDDEN_MESSAGE_403)
        # if the username is found, we can authorize the call
        user = get_user_model().objects.get(username=response.data["username"])
    # closing access to anonymous users
    if user and user.is_anonymous:
        return HttpResponseForbidden(FORBIDDEN_MESSAGE_403)

    rule_filters = {"resource__slug": request_path, "active": True}
    if not user.is_superuser:
        # checking the access rule for the user
        rule_filters["role__in"] = user.get_roles()

    rules = AccessRule.objects.filter(**rule_filters)

    # if the rule does not exists for the user, the request is denined
    if not rules.exists():
        raise Http404("Requested service does not exists")

    # if exists, we can retrieve the upstream url to be proxed to
    proxy_to_url = rules.first().resource

    # if the url is not set, an error is raised
    if proxy_to_url.url_required():
        if not proxy_to_url.url:
            raise Exception("Cannot prox to a url without the url set in the resorce")

        # if everything is fine, the proxy view is prepared
        proxy_view = ProxyView.as_view(upstream=proxy_to_url.url)

        # this function return the dispatch of the response
        return proxy_view(request, **{"path": ""})

    return HttpResponse(status=204)
