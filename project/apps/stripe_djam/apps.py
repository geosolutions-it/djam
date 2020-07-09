from django.apps import AppConfig


class StripeDjamConfig(AppConfig):
    name = "apps.stripe_djam"
    verbose_name = "Stripe Payments DJAM Module"

    def ready(self):
        from . import settings as defaults
        from django.conf import settings

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
