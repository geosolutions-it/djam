from django.apps import AppConfig


class ProjectChecksConfig(AppConfig):
    """
    Pseudo application implementing project checks.
    """

    name = 'checks'
    verbose_name = "Project checks"

    def ready(self):
        import checks.configuration_check
