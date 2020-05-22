from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, re_path, include, reverse_lazy
from django.conf import settings

urlpatterns = [
    re_path(
        "^$", RedirectView.as_view(url=reverse_lazy(settings.HOME_VIEW)), name="home"
    ),
    path(r"admin/", admin.site.urls),
    path("", include("apps.user_management.urls")),
    path(f"{settings.OPENID_URL_PREFIX}/", include("apps.identity_provider.urls")),
    path("", include("apps.privilege_manager.urls")),

    # expose it for browsable api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # here expose endpoints for browsable api
    path("public_api/", include("apps.user_management.api.urls")),
]
