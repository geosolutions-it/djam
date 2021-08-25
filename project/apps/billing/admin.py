from apps.billing.forms import SubscriptionForm
from apps.billing.models import Company, Subscription
from django.contrib import admin


# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = ["company_name", "users"]
