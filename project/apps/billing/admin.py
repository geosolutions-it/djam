from apps.billing.forms import SubscriptionForm
from apps.billing.models import Subscription
from django.contrib import admin


# Register your models here.

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ['start_timestamp']
    fields = ["company_name", "start_timestamp", "end_timestamp", "subscription_type", "groups", "users"]
    list_display = ("id", "company_name", "is_active", "start_timestamp", "end_timestamp", "subscription_type", "permission_group", "related_user")
    ordering = ("-id",)

    form = SubscriptionForm

    def permission_group(self, sub):
        return ", ".join([str(p) for p in sub.groups.all()])

    def related_user(self, sub):
        return ", ".join([str(p) for p in sub.users.all()])

    def is_active(self, sub):
        return sub.is_active()

    is_active.boolean = True