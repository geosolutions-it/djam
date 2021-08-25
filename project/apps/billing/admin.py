from apps.billing.models import Company
from django.contrib import admin


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = ["company_name", "users"]
