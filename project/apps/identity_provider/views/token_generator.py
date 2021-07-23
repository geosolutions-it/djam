from django.http.response import JsonResponse
from apps.identity_provider.models import ApiKey
from rest_framework import permissions, views
from datetime import datetime


class ApiKeyManager(permissions.IsAuthenticated, views.APIView):
    queryset = ApiKey.objects.none()

    def post(self, request):
        user = request.user
        token, created = ApiKey.objects.get_or_create(
            user=user, last_modified=datetime.utcnow()
        )
        return JsonResponse(
            {
                "token": token.key,
                "created": created,
                "last_modified": token.last_modified,
            },
            status=200,
        )

    def put(self, request):
        user = request.user
        token = ApiKey.objects.filter(user=user)
        if token:
            token.delete()
        token, created = ApiKey.objects.get_or_create(
            user=user, last_modified=datetime.utcnow()
        )
        return JsonResponse(
            {
                "token": token.key,
                "created": created,
                "last_modified": token.last_modified,
            },
            status=200,
        )

    def delete(self, request):
        user = request.user
        token = ApiKey.objects.filter(user=user)
        if token:
            token.delete()
            status = 200
        else:
            status = 500
        return JsonResponse(data={}, status=status)
