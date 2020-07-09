from django.apps import AppConfig


class IdentityProviderConfig(AppConfig):
    name = "apps.identity_provider"
    verbose_name = "Identity Provider"

    def ready(self):
        from . import settings as defaults
        from django.conf import settings

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
