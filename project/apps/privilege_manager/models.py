from __future__ import unicode_literals

import logging

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from oidc_provider.models import Client


logger = logging.getLogger(__name__)


class Group(models.Model):
    """
    v1 version of AuthZ Group model of Djam - for MVP only RBAC is supported
    """

    name = models.CharField(max_length=30)
    users = models.ManyToManyField(get_user_model(), blank=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=get_user_model())
def assign_user_to_default_permission_group(sender, instance, created, **kwargs):

    if created and settings.DEFAULT_USER_PERMISSION_GROUP_NAME is not None:
        logging.info(
            f'User Creation: Trying to assign user "{instance.username}" to default permission group "{settings.DEFAULT_USER_PERMISSION_GROUP_NAME}"'
        )

        try:
            default_group = Group.objects.get(
                name=settings.DEFAULT_USER_PERMISSION_GROUP_NAME
            )
        except models.ObjectDoesNotExist:
            logging.info(
                f'User Creation: No "{settings.DEFAULT_USER_PERMISSION_GROUP_NAME}" group found. '
                f'User "{instance.username}" assignment to the default group failed.'
            )
            return

        default_group.users.add(instance)
        default_group.save()


class OpenIdLoginPrevention(models.Model):
    """
    v1 internal Djam policy enforcer preventing OIDC login to certain clients
    """

    oidc_client = models.OneToOneField(Client, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)

    class Meta:
        verbose_name = "OpenID Login Prevention"
        verbose_name_plural = "OpenID Login Preventions"

    def __str__(self):
        return self.oidc_client.name
