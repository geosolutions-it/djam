from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    name = "apps.billing"
    verbose_name = "Subscription Manager"

    def ready(self):
        from . import settings as defaults
        from django.conf import settings

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
