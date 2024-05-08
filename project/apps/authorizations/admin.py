from django.contrib import admin

from apps.authorizations.models import AccessRule, Resource, Role


admin.site.register(AccessRule)
admin.site.register(Resource)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "user",
        "team",
    )