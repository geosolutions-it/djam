from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    name = "apps.user_management"
    verbose_name = "User management"

    def ready(self):
        # add default app settings to project settings
        from apps.user_management import settings as defaults
        from django.conf import settings

        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                # if setting is not present in settings, update settings with it
                setattr(settings, name, getattr(defaults, name))
            elif hasattr(settings, name) and name == "AUTHENTICATION_BACKENDS":
                # merge settings for AUTHENTICATION_BACKENDS (without duplications) to enable email based login,
                # along with other (e.g. username) login backends
                setattr(
                    settings,
                    name,
                    tuple(
                        set(
                            list(getattr(defaults, name))
                            + list(getattr(settings, name))
                        )
                    ),
                )
