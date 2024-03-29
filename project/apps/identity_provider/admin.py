from django.contrib import admin
from apps.identity_provider.models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "key", "last_modified")
    ordering = ("user",)
    search_fields = ("user",)
