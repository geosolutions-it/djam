from django.apps import AppConfig


class PrivilegeManagerConfig(AppConfig):
    name = 'apps.privilege_manager'
    verbose_name = 'Privilege Manager'

    def ready(self):
        # add default app settings to project settings
        from apps.user_management import settings as defaults
        from django.conf import settings
        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                # if setting is not present in settings, update settings with it
                setattr(settings, name, getattr(defaults, name))
