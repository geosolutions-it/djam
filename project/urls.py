from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('apps.user_management.urls')),
    path(f'{settings.OPENID_URL_PREFIX}/', include('apps.identity_provider.urls')),
]
