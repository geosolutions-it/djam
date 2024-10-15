from django.http.response import JsonResponse
from apps.identity_provider.models import ApiKey, default_expiration_date
from rest_framework.permissions import IsAuthenticated
from apps.identity_provider.authentication import DjamTokenAuthentication
from apps.identity_provider.permissions import APIKeyManagementResourceKeyVerification, ExpirationDateValidation
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from apps.identity_provider.utils import select_user, get_apikeys, create_apikey, key_status, key_revoke, key_renew, key_rotate

from rest_framework import serializers
from drf_spectacular.utils import extend_schema, inline_serializer

class ApiKeyView(ViewSet):
    queryset = ApiKey.objects.none()
    authentication_classes = [DjamTokenAuthentication]
    permission_classes = [IsAuthenticated, ExpirationDateValidation, APIKeyManagementResourceKeyVerification]

    # Remove the resource key permissions from /create_key and /key_list endpoints
    def get_permissions(self):
        if self.action in ('create_key', 'key_list'):
            self.permission_classes = [IsAuthenticated, ExpirationDateValidation]
        return super(self.__class__, self).get_permissions()

    # Spectacular - Swagger: Data content for key_list endpoint
    @extend_schema(
             request={
                 "application/json": inline_serializer(
                name="KeyListSchemaSerializer",
                fields={
                    "account_id": serializers.IntegerField(default="null"),
                 },
             ),
            }
         )
    
    # ApiKeyView actions
    @action(detail=False, methods=['post'])
    def key_list(self, request):
        ''' 
        The user is able to export her/his keys with
        resource scope.
        '''
        
        user = request.user
        if user.is_superuser:
            user = select_user(request, user)
            data = {
                   "tokens of {}".format(user): get_apikeys(user),
                   }
            status=200
            return JsonResponse(data, status=status)
        elif request.user.is_superuser == False:
            data = {
                   "tokens of {}".format(user): get_apikeys(user),
                   }
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)
    
    # Spectacular - Swagger: Data content for create_key endpoint
    @extend_schema(
             request={
                 "application/json": inline_serializer(
                name="CreateKeySchemaSerializer",
                fields={
                    "revoked": serializers.CharField(default="False"),
                    "expiry": serializers.DateTimeField(default=default_expiration_date()),
                    "account_id": serializers.IntegerField(default="null"),
                 },
             ),
            }
         )

    @action(detail=False, methods=['post'])
    def create_key(self, request):
        ''' 
        The user is able to create a key with
        resource scope.
        '''

        user = request.user
        if user.is_superuser:
            user = select_user(request, user)
            data = create_apikey(request, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = create_apikey(request, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)
        
    # Spectacular - Swagger: Data content for status endpoint
    @extend_schema(
             request={
                 "application/json": inline_serializer(
                name="StatusSchemaSerializer",
                fields={
                    "resource_key": serializers.CharField(required=True),
                    "account_id": serializers.IntegerField(default="null"),
                 },
             ),
            }
         )
    
    @action(detail=False, methods=['post'])
    def status(self, request):
        ''' 
        The user is able to export the status of
        a resource key.
        '''
        
        user = request.user
        resource_key = request.data.get('resource_key', None)
        
        if user.is_superuser:
            user = select_user(request, user)
            data = key_status(resource_key, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = key_status(resource_key, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)     
    
    # Spectacular - Swagger: Data content for revoke endpoint
    @extend_schema(
             request={
                 "application/json": inline_serializer(
                name="RevokeSchemaSerializer",
                fields={
                    "resource_key": serializers.CharField(required=True),
                    "revoked": serializers.CharField(default="False"),
                    "account_id": serializers.IntegerField(default="null"),
                 },
             ),
            }
         )
    
    @action(detail=False, methods=['post'])
    def revoke(self, request):
        '''
        The user is able to revoke her/his resource key
        '''
        
        user = request.user
        resource_key = request.data.get('resource_key', None)
        revoked = request.data.get('revoked', None)
        
        if user.is_superuser:
            user = select_user(request, user)
            data = key_revoke(resource_key, revoked, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = key_revoke(resource_key, revoked, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)
        
    # Spectacular - Swagger: Data content for renew endpoint
    @extend_schema(
             request= {
                "application/json":inline_serializer(
                name="RenewSchemaSerializer",
                fields={
                    "resource_key": serializers.CharField(required=True),
                    "expiry": serializers.DateTimeField(default=default_expiration_date()),
                    "account_id": serializers.IntegerField(default="null"),
                 },
             ),
            }

         )
    
    @action(detail=False, methods=['post'])
    def renew(self, request):
        ''' 
        The user is able to renew the expiration date
        of a resource key.
        '''

        user = request.user
        resource_key = request.data.get('resource_key', None)
        expiry = request.data.get('expiry', None)
        
        if user.is_superuser:
            user = select_user(request, user)
            data = key_renew(resource_key, expiry, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = key_renew(resource_key, expiry, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)
    
    # Spectacular - Swagger: Data content for rotate endpoint
    @extend_schema(
             request={
                 "application/json": inline_serializer(
                name="RotateSchemaSerializer",
                fields={
                    "resource_key": serializers.CharField(required=True),
                    "short_expiry": serializers.CharField(default="False"),
                    "account_id": serializers.IntegerField(default="null"),
                 },
             ),
            }
         )
    
    @action(detail=False, methods=['post'])
    def rotate(self, request):
        ''' 
        The user is able to revoke an old resource key
        and create a new one. Optionaly she/he can extend
        the expiration date of her/his old resource key
        for three days by setting the "short_expiry" to True.
        '''

        user = request.user
        resource_key = request.data.get('resource_key', None)
        # A new short expiration date for the old key
        short_expiry = request.data.get('short_expiry', None)
        
        if user.is_superuser:
            user = select_user(request, user)
            data = key_rotate(resource_key, short_expiry, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = key_rotate(resource_key, short_expiry, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)