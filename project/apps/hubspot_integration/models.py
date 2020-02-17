from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save


@receiver(pre_save, sender=get_user_model())
def register_user_in_hubspot(sender, instance, **kwargs):
    if not settings.REGISTER_USERS_WITH_CONSENT_IN_HUBSPOT:
        # get_user_model().objects.filter(email=instance.email)
        return

    # if in user model consent changed to True, register the user in Hubspot
