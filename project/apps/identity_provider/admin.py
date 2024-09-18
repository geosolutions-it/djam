from django.contrib import admin
from apps.identity_provider.models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("user", "key", "scope", "revoked", "expiry")
    ordering = ("user",)
    search_fields = ("user",)
    list_filter = ["revoked", "scope"]
