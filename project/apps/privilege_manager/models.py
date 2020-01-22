from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model


class Group(models.Model):
    """
    v1 version of AuthZ Group model of Djam - for MVP only RBAC is supported
    """
    user = models.ManyToManyField(get_user_model())
    name = models.CharField(max_length=30, blank=True)
