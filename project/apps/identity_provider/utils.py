import random
import string
import logging

from datetime import datetime

from django.urls import reverse
from django.http import request
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from apps.identity_provider import models

logger = logging.getLogger(__name__)


def random_string(length=25):
    """Generate a random string of fixed length """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_activation_link(username: str, request: request):

    UserModel = get_user_model()

    user = UserModel.objects.filter(username=username).first()
    if user is None:
        logger.error(f'Activation link generator: No user found with username "{username}"')
        return

    try:
        # Check whether the activation code exist
        activation_code = user.useractivationcode

        activation_code.activation_code = random_string()
        activation_code.created_at = datetime.now()
        activation_code.save()
        logger.info(f'Activation link generator: Activation code for "{username}" was regenerated.')

    except models.UserActivationCode.DoesNotExist:
        logger.info(f'Activation link generator: No activation code found for "{username}". Creating a new activation code.')
        models.UserActivationCode.objects.create(user=user)

    request_schema = 'https://' if request.is_secure() else 'http://'
    query_parameter = f'?activation_code={user.useractivationcode.activation_code}'
    activation_url = request_schema + get_current_site(request).domain + reverse('email_confirmation',
                                                                                 kwargs={'user_uuid': user.uuid}) + query_parameter

    return activation_url
