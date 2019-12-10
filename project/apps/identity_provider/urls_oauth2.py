from django.urls import path, re_path, include
from oauth2_provider import views as oauth2_views
from django.contrib.auth import get_user_model
from apps.identity_provider.utils import non_anonymous_user_passes_test


# required for user_passes_test proper work
User = get_user_model()

base_oauth2_urlpatterns = [
    path(r'authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path(r'token/', oauth2_views.TokenView.as_view(), name="token"),
    path(r'revoke_token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
    path(r'introspect/', oauth2_views.IntrospectTokenView.as_view(), name="revoke-token"),
]

# Protect OAuth2 management access
management_oauth2_urlpatterns = [
    path(r'applications/', non_anonymous_user_passes_test(lambda u: u.is_staff)(oauth2_views.ApplicationList.as_view()), name="list"),
    path(r'applications/register/', non_anonymous_user_passes_test(lambda u: u.is_staff)(oauth2_views.ApplicationRegistration.as_view()), name="register"),
    path(r'applications/<int:pk>/', non_anonymous_user_passes_test(lambda u: u.is_staff)(oauth2_views.ApplicationDetail.as_view()), name="detail"),
    path(r'applications/<int:pk>/delete/', non_anonymous_user_passes_test(lambda u: u.is_staff)(oauth2_views.ApplicationDelete.as_view()), name="delete"),
    path(r'applications/<int:pk>/update/', non_anonymous_user_passes_test(lambda u: u.is_staff)(oauth2_views.ApplicationUpdate.as_view()), name="update"),
    # Token management views
    path(r"authorized_tokens/", non_anonymous_user_passes_test(lambda u: u.is_staff)(oauth2_views.AuthorizedTokensListView.as_view()), name="authorized-token-list"),
    re_path(r"^authorized_tokens/(?P<pk>[\w-]+)/delete/$", non_anonymous_user_passes_test(lambda u: u.is_staff)(oauth2_views.AuthorizedTokenDeleteView.as_view()), name="authorized-token-delete"),
]

oauth2_url_patterns = base_oauth2_urlpatterns + management_oauth2_urlpatterns


urlpatterns = [
    path(r'accounts/', include('django.contrib.auth.urls')),
    path(r'', include((oauth2_url_patterns, 'apps.identity_provider'), namespace='oauth2_provider')),
]
