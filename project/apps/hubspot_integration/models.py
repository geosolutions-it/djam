import logging
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist

from apps.hubspot_integration.utils import send_hubspot_notify, register_login_in_hubspot


logger = logging.getLogger(__name__)

def is_hubspot_configured():
    if not settings.REGISTRATION_EMAIL_CONFIRMATION or settings.REGISTRATION_MODERATION:
        logging.debug('Hubspot registration: SKIPPED. Registration available only for Email Confirmation Registration only flow.')
        return False

    if not settings.REGISTER_USERS_WITH_CONSENT_IN_HUBSPOT:
        logging.debug('Hubspot registration: SKIPPED. Registration is turned off.')
        return False
    return True


@receiver(pre_save, sender=get_user_model())
def register_user_in_hubspot(sender, instance, **kwargs):

    if not is_hubspot_configured():
        return

    try:
        db_user = get_user_model().objects.get(email=instance.email)
    except ObjectDoesNotExist:
        logging.debug(f'Hubspot registration: SKIPPED. User with "{instance.email}" email does not exist in the DB yet.')
        return

    if db_user.consent and not db_user.email_confirmed and instance.email_confirmed:
        # user gave their consent at registration, and now their email is confirmed
        logging.info(f'Hubspot registration: registering user with email "{instance.email}" in Hubspot.')
        send_hubspot_notify(instance.email, instance.username, instance.consent, instance.first_name, instance.last_name)


@receiver(user_logged_in)
def register_user_login_in_hubspot(sender, user, request, **kwargs):
    if not is_hubspot_configured():
        return

    if user.consent and user.email_confirmed:
        # user gave their consent at registration, and now their email is confirmed
        logging.info(f'Hubspot user login event: registering a user login with email "{user.email}" in Hubspot.')
        register_login_in_hubspot(user.email)
