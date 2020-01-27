from django.contrib import admin
from apps.privilege_manager.models import Group
from django.contrib.auth.models import Group as DefaultGroup


# un-registration of Django auth Group model in admin page
admin.site.unregister(DefaultGroup)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

