from django.apps import AppConfig


class HubspotIntegrationConfig(AppConfig):
    name = "apps.hubspot_integration"
    verbose_name = "Hubspot Integration"

    def ready(self):
        from . import settings as defaults
        from django.conf import settings

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
