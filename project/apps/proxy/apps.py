from django.apps import AppConfig


class ProxyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.proxy"

    def ready(self):
        from . import settings as defaults
        from django.conf import settings

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
