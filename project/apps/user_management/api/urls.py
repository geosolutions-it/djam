from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.user_management.api.views import UserViewSet

router = DefaultRouter()

router.register('users', UserViewSet, basename='fetch_users')

urlpatterns = [
    path('', include(router.urls))
]
