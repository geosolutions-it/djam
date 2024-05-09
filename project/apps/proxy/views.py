from urllib.parse import urlparse
from django.http import Http404
from apps.authorizations.models import AccessRule
from revproxy.views import ProxyView


def proxy_view(request, request_path):
    '''
    Will prox the request to a service defined in the admin
    only the users/team with right access can see the proxed response
    '''
    # closing access to anonymous users
    if request.user and request.user.is_anonymous:
        raise Http404
    
    # getting the URL as object
    rule_path = urlparse(request.get_full_path_info())

    # if some query param is available, is re-merged in the path
    if rule_path.query:
        request_path = f"{request_path}?{rule_path.query}"
    
    # checking the access rule for the user

    rules = AccessRule.objects\
        .filter(resource__path=request_path)\
        .filter(role__in=request.user.get_role())\
        .filter(active=True)

    # if the rule does not exists for the user, the request is denined
    if not rules.exists():
        raise Http404

    # if exists, we can retrieve the upstream url to be proxed to
    proxy_to_url = rules.first().resource.url
    
    # if the url is not set, an error is raised
    if proxy_to_url is None:
        raise Exception("Cannot prox to a url without the url set in the resorce")
    
    # if everything is fine, the proxy view is prepared
    proxy_view = ProxyView.as_view(upstream=proxy_to_url)

    # this function return the dispatch of the response
    return proxy_view(request, **{"path": request_path})
