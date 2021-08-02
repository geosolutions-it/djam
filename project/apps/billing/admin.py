from apps.billing.forms import SubscriptionForm
from apps.billing.models import Subscription
from django.contrib import admin


# Register your models here.

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ['start_timestamp']
    fields = ["company_name", "start_timestamp", "end_timestamp", "subscription_type", "groups", "users"]
    list_display = ("id", "company_name", "start_timestamp", "end_timestamp", "subscription_type", "get_group", "get_users")
    ordering = ("end_timestamp",)

    form = SubscriptionForm

    def get_group(self, sub):
        return ", ".join([str(p) for p in sub.groups.all()])

    def get_users(self, sub):
        return ", ".join([str(p) for p in sub.users.all()])
