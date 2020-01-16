from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    name = 'apps.user_management'
    verbose_name = 'User management'

    def ready(self):
        from apps.user_management import settings as defaults
        from django.conf import settings
        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
