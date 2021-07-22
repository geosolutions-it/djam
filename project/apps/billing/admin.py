from apps.billing.models import Billing
from django.contrib import admin

# Register your models here.

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "expiry_date")
    ordering = ("user",)
    search_fields = ("user",)
