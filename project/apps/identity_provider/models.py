from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sessions.base_session import AbstractBaseSession
import logging

logger = logging.getLogger(__name__)


class Session(AbstractBaseSession):
    uuid = models.UUIDField(db_index=True, default=uuid4)
    user_id = models.IntegerField(db_index=True, null=True)
    oidc_code = models.CharField(null=True, max_length=256)

    @classmethod
    def get_session_store_class(cls):
        from apps.identity_provider.session_backend import SessionStore

        return SessionStore


class ApiKey(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text="API key will have the same privilege groups as it's owner.",
    )
    key = models.UUIDField(null=False, blank=False, default=uuid4)
    revoked = models.BooleanField(
        null=False,
        default=False,
        help_text="If the API key is revoked, clients cannot use it.",
    )

    def save(self, *args, **kwargs):
        if not self.pk and ApiKey.objects.filter(user=self.user, revoked=False).exists():
            # we might create new ApiKey but user already has one valid
            logger.info(f'User {self.user.username} already has active API Key. Skipping')
            # get is intentional. exception here is mistake in logic
            api_key = ApiKey.objects.get(user=self.user, revoked=False)
            self.pk = api_key.pk
            self.key = api_key.key
            # this is to force update if possible
            kwargs.update({'force_insert': False})
            super(ApiKey, self).save(*args, **kwargs)
        else:
            # pk exists, then we are in update, we want to save. or user doesnt have valid keys
            super(ApiKey, self).save(*args, **kwargs)
