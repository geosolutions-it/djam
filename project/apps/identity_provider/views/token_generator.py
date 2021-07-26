from django.http.response import JsonResponse
from apps.identity_provider.models import ApiKey
from rest_framework import permissions, views
from datetime import datetime


class ApiKeyManager(permissions.IsAuthenticated, views.APIView):
    queryset = ApiKey.objects.none()

    def post(self, request):
        user = request.user
        if self._is_a_free_user(user):
            data={}
            status=403
        else:
            token, created = ApiKey.objects.get_or_create(
                user=user, last_modified=datetime.utcnow()
            )
            data = {
                "token": token.key,
                "created": created,
                "last_modified": token.last_modified,
            }
            status=200
        return JsonResponse(data, status=status)

    def put(self, request):
        user = request.user
        if self._is_a_free_user(user):
            data={}
            status=403
        else:
            token = ApiKey.objects.filter(user=user)
            if token:
                token.delete()
            token, created = ApiKey.objects.get_or_create(
                user=user, last_modified=datetime.utcnow()
            )
            data = {
                "token": token.key,
                "created": created,
                "last_modified": token.last_modified,
            }
            status=200
        return JsonResponse(data, status=status)


    def delete(self, request):
        user = request.user
        if self._is_a_free_user(user):
            status=403
        else:
            token = ApiKey.objects.filter(user=user)
            if token:
                token.delete()
                status = 200
            else:
                status = 500
        return JsonResponse(data={}, status=status)

    def _is_a_free_user(self, user):
        return 'free' in [g.name.lower() for g in user.group_set.all()] 