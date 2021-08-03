from apps.billing.enums import SubscriptionTypeEnum
from django.http.response import JsonResponse
from apps.identity_provider.models import ApiKey
from rest_framework import permissions, views
from datetime import datetime


class ApiKeyManager(permissions.IsAuthenticated, views.APIView):
    queryset = ApiKey.objects.none()

    def post(self, request):
        user = request.user
        if self._user_is_authorized(user):
            token, created = ApiKey.objects.get_or_create(
                user=user, last_modified=datetime.utcnow()
            )
            data = {
                "token": token.key,
                "created": created,
                "last_modified": token.last_modified,
            }
            status=200
        else:
            data={}
            status=403
        return JsonResponse(data, status=status)

    def put(self, request):
        user = request.user
        if self._user_is_authorized(user):
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
        else:
            data={}
            status=403
        return JsonResponse(data, status=status)


    def delete(self, request):
        user = request.user
        if self._user_is_authorized(user):
            token = ApiKey.objects.filter(user=user)
            if token:
                token.delete()
                status = 200
            else:
                status = 500
        else:
            status=403
        return JsonResponse(data={}, status=status)

    def _user_is_authorized(self, user):
        group = user.group_set.all()
        if group.exists():
            if group.first().name.lower() == 'admin':
                return True
            else:
                return 'ENTERPRISE' in user.get_group()
        return False