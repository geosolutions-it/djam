from datetime import datetime
from django.utils import timezone
from apps.identity_provider.settings import SHORT_APIKEY_EXPIRE
from apps.identity_provider.models import ApiKey, default_expiration_date
from apps.user_management.models import User

# Helper function for selecting a simple user   
def select_user(request, user):
    other_user = request.data.get("account_id", None)
    if other_user:
        founded_user = User.objects.filter(id=other_user)
        if founded_user.exists():
            user = founded_user.get()
    return user

# Endpoints functionality
def get_apikeys(user):
    # A user cannot create a management key
        
    # Find keys of a user with the scope resource
    apikeys = ApiKey.objects.filter(user=user).filter(scope='resource')

    return apikeys
    
def create_apikey(request, user):
    # A user cannot create a management key
    scope = 'resource'
    revoked = request.data.get('revoked', False)
    expiry = request.data.get('expiry', default_expiration_date())

    record = ApiKey.objects.create(user=user, scope=scope, revoked=revoked, expiry=expiry)
        
    data = {
        "username": str(user),
        "token": record.key,
        "id": record.id,
        "created": "success",
    }    
    return(data)
    
def key_status(resource_key, user):
        
    resource_key_obj = ApiKey.objects.filter(user=user).filter(scope='resource').get(key=resource_key)
        
    data = {
        "username" : str(user),
        "key": resource_key_obj.key,
        "id": resource_key_obj.id,
        "revoked": resource_key_obj.revoked,
        "expiration date":  resource_key_obj.expiry
    }   
    return(data)
    
def key_revoke(resource_key, revoked, user):
        
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
        
def key_renew(resource_key, expiry, user):
        
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
        
def key_rotate(resource_key, short_expiry, user):
        
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