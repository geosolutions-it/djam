from django.urls import path, include


urlpatterns = [
    path('', include('oidc_provider.urls', namespace='oidc_provider')),
]
