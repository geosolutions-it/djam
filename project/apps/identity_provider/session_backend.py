from django.contrib.sessions.backends.db import SessionStore as DBStore


class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls):
        from apps.identity_provider.models import Session
        return Session

    def create_model_instance(self, data):
        """
        On session creation update user_id column in the database (session table).
        """
        obj = super().create_model_instance(data)
        try:
            user_id = int(data.get('_auth_user_id'))
        except (ValueError, TypeError):
            user_id = None
        obj.user_id = user_id
        return obj
