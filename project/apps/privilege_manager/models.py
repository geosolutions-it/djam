from __future__ import unicode_literals

import logging

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import Group
from oidc_provider.models import Client

from apps.authorizations.models import Role


logger = logging.getLogger(__name__)


class Team(Group):
    """
    v1 version of AuthZ Group model of Djam - for MVP only RBAC is supported
    """

    role = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

class OpenIdLoginPrevention(models.Model):
    """
    v1 internal Djam policy enforcer preventing OIDC login to certain clients
    """

    oidc_client = models.OneToOneField(Client, on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team, blank=True)

    class Meta:
        verbose_name = "OpenID Login Prevention"
        verbose_name_plural = "OpenID Login Preventions"

    def __str__(self):
        return self.oidc_client.name
