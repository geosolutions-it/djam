from django.apps import AppConfig


class AdminConfig(AppConfig):
    name = "apps.administration"
    verbose_name = "Client Management Module"

    def ready(self):
        from . import settings as defaults
        from django.conf import settings

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
