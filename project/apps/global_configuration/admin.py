from django.contrib import admin

from apps.global_configuration.models import GlobalConfiguration


@admin.register(GlobalConfiguration)
class GlobalConfigurationAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        # Since model is not deletable, lets hide deletion possibility in the admin
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # allow only superusers to modify Configuration
        if not request.user.is_superuser:
            for field in form.base_fields:
                form.base_fields.get(field).disabled = True

        return form
