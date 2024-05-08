from django.contrib import admin
from apps.privilege_manager.models import Team, OpenIdLoginPrevention
from django.contrib.auth.models import Group as DefaultGroup

# un-registration of Django auth Group model in admin page
admin.site.unregister(DefaultGroup)
admin.site.register(OpenIdLoginPrevention)

@admin.register(Team)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)
