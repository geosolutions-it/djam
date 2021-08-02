from apps.billing.models import Subscription
from django.contrib import admin

# Register your models here.

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "start_timestamp", "end_timestamp", "subscription_type")
    ordering = ("end_timestamp",)
