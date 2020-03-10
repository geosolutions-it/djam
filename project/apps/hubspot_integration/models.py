import logging
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.core.exceptions import ObjectDoesNotExist

from apps.hubspot_integration.utils import send_hubspot_notify


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=get_user_model())
def register_user_in_hubspot(sender, instance, **kwargs):

    if not settings.REGISTRATION_EMAIL_CONFIRMATION or settings.REGISTRATION_MODERATION:
        logging.debug('Hubspot registration: SKIPPED. Registration available only for Email Confirmation Registration only flow.')
        return

    if not settings.REGISTER_USERS_WITH_CONSENT_IN_HUBSPOT:
        logging.debug('Hubspot registration: SKIPPED. Registration is turned off.')
        return

    try:
        db_user = get_user_model().objects.get(email=instance.email)
    except ObjectDoesNotExist:
        logging.debug(f'Hubspot registration: SKIPPED. User with "{instance.email}" email does not exist in the DB yet.')
        return

    if instance.email_confirmed:
        # user gave their consent at registration, and now their email is confirmed
        logging.info(f'Hubspot registration: registering user with email "{instance.email}" in Hubspot.')
        send_hubspot_notify(instance.email, instance.username, instance.consent, instance.first_name, instance.last_name)
