from django.http.response import JsonResponse
from apps.identity_provider.models import ApiKey, default_expiration_date
from apps.user_management.models import User
from rest_framework.permissions import IsAuthenticated
from apps.identity_provider.authentication import DjamTokenAuthentication
from apps.identity_provider.permissions import APIKeyManagementResourceKeyVerification, ExpirationDateValidation
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from datetime import datetime
from django.utils import timezone
from apps.identity_provider.settings import SHORT_APIKEY_EXPIRE
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
             request=inline_serializer(
                name="KeyListSchemaSerializer",
                fields={
                    "account_id": serializers.IntegerField(),
                 },
             ),
         )
    
    # ApiKeyView actions
    @action(detail=False, methods=['post'])
    def key_list(self, request):
        
        user = request.user
        if user.is_superuser:
            user = self._select_user(request, user)
            data = self._key_list(user)
            status=200
            return JsonResponse(data, status=status)
        elif request.user.is_superuser == False:
            data = self._key_list(user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)
    
    # Spectacular - Swagger: Data content for create_key endpoint
    @extend_schema(
             request=inline_serializer(
                name="CreateKeySchemaSerializer",
                fields={
                    "resource_key": serializers.CharField(required=True),
                    "revoked": serializers.CharField(default="False"),
                    "expiry": serializers.DateTimeField(default=default_expiration_date()),
                    "account_id": serializers.IntegerField(default=0),
                 },
             ),
         )

    @action(detail=False, methods=['post'])
    def create_key(self, request):
        
        user = request.user
        if user.is_superuser:
            user = self._select_user(request, user)
            data = self._create_key(request, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = self._create_key(request, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)
        
    # Spectacular - Swagger: Data content for status endpoint
    @extend_schema(
             request=inline_serializer(
                name="StatusSchemaSerializer",
                fields={
                    "resource_key": serializers.CharField(required=True),
                    "account_id": serializers.IntegerField(default=0),
                 },
             ),
         )
    
    @action(detail=False, methods=['post'])
    def status(self, request):
        
        user = request.user
        resource_key = request.data.get('resource_key', None)
        
        if user.is_superuser:
            user = self._select_user(request, user)
            data = self._key_status(resource_key, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = self._key_status(resource_key, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)     
    
    # Spectacular - Swagger: Data content for revoke endpoint
    @extend_schema(
             request=inline_serializer(
                name="RevokeSchemaSerializer",
                fields={
                    "resource_key": serializers.CharField(required=True),
                    "revoked": serializers.CharField(default="False"),
                    "account_id": serializers.IntegerField(default=0),
                 },
             ),
         )
    
    @action(detail=False, methods=['post'])
    def revoke(self, request):
        
        user = request.user
        resource_key = request.data.get('resource_key', None)
        revoked = request.data.get('revoked', None)
        
        if user.is_superuser:
            user = self._select_user(request, user)
            data = self._key_revoke(resource_key, revoked, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = self._key_revoke(resource_key, revoked, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)
        
    # Spectacular - Swagger: Data content for renew endpoint
    @extend_schema(
             request=inline_serializer(
                name="RenewSchemaSerializer",
                fields={
                    "resource_key": serializers.CharField(required=True),
                    "expiry": serializers.DateTimeField(default=default_expiration_date()),
                    "account_id": serializers.IntegerField(default=0),
                 },
             ),
         )
    
    @action(detail=False, methods=['post'])
    def renew(self, request):
        
        user = request.user
        resource_key = request.data.get('resource_key', None)
        expiry = request.data.get('expiry', None)
        
        if user.is_superuser:
            user = self._select_user(request, user)
            data = self._key_renew(resource_key, expiry, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = self._key_renew(resource_key, expiry, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)
    
    # Spectacular - Swagger: Data content for rotate endpoint
    @extend_schema(
             request=inline_serializer(
                name="RotateSchemaSerializer",
                fields={
                    "resource_key": serializers.CharField(required=True),
                    "short_expiry": serializers.BooleanField(default=False),
                    "account_id": serializers.IntegerField(default=0),
                 },
             ),
         )
    
    @action(detail=False, methods=['post'])
    def rotate(self, request):
        
        user = request.user
        resource_key = request.data.get('resource_key', None)
        # A new short expiration date for the old key
        short_expiry = request.data.get('short_expiry', None)
        
        if user.is_superuser:
            user = self._select_user(request, user)
            data = self._key_rotate(resource_key, short_expiry, user)
            status=200
            return JsonResponse(data, status=status)
        elif user.is_superuser == False:
            data = self._key_rotate(resource_key, short_expiry, user)
            status=200
            return JsonResponse(data, status=status)
        else:
            data = {}
            status=403
            return JsonResponse(data, status=status)
    

    # Helper function for selecting a simple user   
    def _select_user(self, request, user):
        other_user = request.data.get("account_id", None)
        if other_user:
            founded_user = User.objects.filter(id=other_user)
            if founded_user.exists():
                user = founded_user.get()
        return user
    
    # Endpoints functionality
    def _key_list(self, user):
        # A user cannot create a management key
        
        # Find keys of a user with the scope resource
        user_tokens = ApiKey.objects.filter(user=user).filter(scope='resource')

        # Create a list with the resource keys of this user
        token_list = [i.key for i in user_tokens]
        
        data = {
            "tokens of {}".format(user): token_list,
        }    
        return(data)
    
    def _create_key(self, request, user):
        # A user cannot create a management key
        scope = 'resource'
        revoked = request.data.get('revoked', False)
        expiry = request.data.get('expiry', default_expiration_date())

        record = ApiKey.objects.create(user=user, scope=scope, revoked=revoked, expiry=expiry)
        
        data = {
            "token": record.key,
            "id": record.id,
            # "wms_token": token.wms_key,
            "created": "success",
            #"last_modified": token.last_modified,
        }    
        return(data)
    
    def _key_status(self, resource_key, user):
        
        '''This method outputs the requested resource key status.
           All the checks for the key verification and
           the user permissions are applied in the permission class: 
           APIKeyManagementResourceKeyVerification'''
        
        resource_key_obj = ApiKey.objects.filter(user=user).filter(scope='resource').get(key=resource_key)
            
        data = {
            "username" : str(user),
            "revoked": resource_key_obj.revoked,
            "expiration date":  resource_key_obj.expiry
        }   
        return(data)
    
    def _key_revoke(self, resource_key, revoked, user):
        
        '''The method set the revoke value to the defined
           resource key. All the checks for the key verification and
           the user permissions are applied in the permission class: 
           APIKeyManagementResourceKeyVerification'''
        
        resource_key_obj = ApiKey.objects.filter(user=user).filter(scope='resource').get(key=resource_key)
        
        if revoked is None:
            data = {
            "message": "Please set a revoked value"}   
            return(data)
        else:
            # Set and save a new revoked value
            resource_key_obj.revoked = revoked
            resource_key_obj.save()

            data = {
                "username" : str(user),
                "key": resource_key_obj.key,
                "id": resource_key_obj.id,
                "new revoked value": resource_key_obj.revoked,
            }   
            return(data)
        
    def _key_renew(self, resource_key, expiry, user):
        
        '''The method extend the expiration date of a resource key.
           All the checks for the key verification and
           the user permissions are applied in the permission class: 
           APIKeyManagementResourceKeyVerification'''
        
        resource_key_obj = ApiKey.objects.filter(user=user).filter(scope='resource').get(key=resource_key)
        
        if expiry is None:
            # set the default expiration date and save it to the database
            resource_key_obj.expiry = default_expiration_date()
            resource_key_obj.save()
            
            data = {
                "username" : str(user),
                "key": resource_key_obj.key,
                "id": resource_key_obj.id,
                "New expiration date": resource_key_obj.expiry,
            }      
            return(data)
        else:
            # Convert date to datetime object with timezone
            expiry_obj = datetime.strptime(expiry, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
            # Set and save a new revoked value
            resource_key_obj.expiry = expiry_obj
            resource_key_obj.save()

            data = {
                "username" : str(user),
                "key": resource_key_obj.key,
                "id": resource_key_obj.id,
                "New expiration date": resource_key_obj.expiry,
            }   
            return(data)
        
    def _key_rotate(self, resource_key, short_expiry, user):
        
        '''The method set the revoked value of th resource key to false,
           creates a new one and extend the expiration date of a old key
           to some hours or days.
           All the checks for the key verification and
           the user permissions are applied in the permission class: 
           APIKeyManagementResourceKeyVerification'''
        
        resource_key_obj = ApiKey.objects.filter(user=user).filter(scope='resource').get(key=resource_key)
        extension = 0

        # Set the revoked value of this key to True
        resource_key_obj.revoked = True
        
        if short_expiry=="True":
            extension = 3
            resource_key_obj.expiry = timezone.now() + SHORT_APIKEY_EXPIRE
            resource_key_obj.save()    
        else:
            resource_key_obj.save()

        # Create a new resource key

        record = ApiKey.objects.create(user=user, scope="resource", revoked=False)

        data = {
            "message": "The old key: {} with id: {} is revoked and extended for {} days".format(resource_key_obj.key, resource_key_obj.id, extension),
            "username": str(user),
            "new_key": record.key,
            "id": record.id,
            }   
        return(data)