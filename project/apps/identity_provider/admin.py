from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.identity_provider.models import ApiKey


class ExpiredKeyFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _("Expired")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "expired"

    def lookups(self, request, model_admin):
        return [
            ("true", _("Expired")),
            ("false", _("Not Expired")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "true":
            return queryset.filter(
                expiry__lt=timezone.now()
            )
        elif self.value() == "false":
            return queryset.filter(
                expiry__gte=timezone.now()
            )
        return queryset
        

@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("user", "key", "scope", "revoked", "expiry")
    ordering = ("user",)
    search_fields = ("user",)
    list_filter = ["revoked", "scope", ExpiredKeyFilter]
