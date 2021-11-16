import apps.user_management.models
from django.http.response import JsonResponse
from apps.identity_provider.models import ApiKey
from apps.privilege_manager.models import Group
from rest_framework import views
from datetime import datetime
from apps.user_management.models import User
from rest_framework.permissions import IsAuthenticated

class ApiKeyManager(views.APIView):
    queryset = ApiKey.objects.none()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if self._user_is_authorized(user):
            user = self._select_user(request, user)
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
            user = self._select_user(request, user)
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
            user = self._select_user(request, user)
            token = ApiKey.objects.filter(user=user)
            if token:
                token.delete()
                status = 200
            else:
                status = 500
        else:
            status=403
        return JsonResponse(data={}, status=status)

    def patch(self, request):
        user = request.user
        message = "Api has been revoked"
        if self._user_is_authorized(user):
            user = self._select_user(request, user)
            token = ApiKey.objects.filter(user=user)
            if token:
                new_value = not token.first().revoked
                token.update(revoked=new_value)
                if not new_value:
                    message = token.first().key
                status = 200
            else:
                status = 500
        else:
            status=403
        return JsonResponse(data={"token": message}, status=status)

    def _user_is_authorized(self, user):
        group = user.get_group()
        if group:
            if group == 'admin' or user.is_superuser:
                return True
            else:
                return 'enterprise' == group
        return False
    
    def _select_user(self, request, user):
        other_user = request.GET.get('account_id', None)
        if other_user:
            founded_user = User.objects.filter(id=other_user)
            if founded_user.exists():
                user = founded_user.get()
        return user
