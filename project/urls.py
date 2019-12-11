from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('apps.identity_provider.urls_user_management')),
    path(f'{settings.OPENID_URL_PREFIX}/', include('apps.identity_provider.urls_openid')),
]
