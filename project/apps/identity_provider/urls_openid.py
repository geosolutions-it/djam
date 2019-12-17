from django.urls import path, include

from .views.oidc_stateless import StatelessAuthorizeView

urlpatterns = [
    path('', include('oidc_provider.urls', namespace='oidc_provider')),
    path('authorize/stateless/', StatelessAuthorizeView.as_view()),
]
