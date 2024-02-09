from apps.billing.models import Company
from django.contrib import admin
from apps.billing.forms import CompanyAdminForm


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    form = CompanyAdminForm
    fields = ["company_name", "users"]
    ordering = ("company_name",)
    search_fields = ("company_name",)
