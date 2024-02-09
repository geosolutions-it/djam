from __future__ import unicode_literals

import logging
from enum import Enum

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

    class GroupNames(Enum):
        FREE = "free"
        PRO = "pro"
        ENTERPRISE = "enterprise"

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


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
