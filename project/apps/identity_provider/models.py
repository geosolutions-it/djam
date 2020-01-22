from uuid import uuid4
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models


class Session(AbstractBaseSession):
    uuid = models.UUIDField(db_index=True, default=uuid4)

    @classmethod
    def get_session_store_class(cls):
        from apps.identity_provider.session_backend import SessionStore
        return SessionStore
