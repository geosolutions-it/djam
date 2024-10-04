from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from apps.user_management.views.account_page import ProfileRedirectView
from revproxy.views import ProxyView

class TestProxyView(ProxyView):
    upstream = 'http://example.com'

urlpatterns = [
    #re_path(r'(?P<path>.*)', ProxyView.as_view(upstream='http://example.com/')),
    re_path("^$", ProfileRedirectView.as_view(), name="home"),
    path(r"admin/", admin.site.urls),
    path("", include("apps.user_management.urls")),
    path("", include("apps.proxy.urls")),
    path(f"{settings.OPENID_URL_PREFIX}/", include("apps.identity_provider.urls")),
    path("", include("apps.privilege_manager.urls")),
    # expose it for browsable api
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # here expose endpoints for browsable api
    path("public_api/", include("apps.user_management.api.urls")),
]
