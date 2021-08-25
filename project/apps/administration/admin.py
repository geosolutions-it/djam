from apps.administration.forms import AccountManagementForm, CompanySubsForm
from apps.administration.admin_filters import (
    IsActiveCustomFilter,
)
from apps.administration.models import AccountManagementModel
from apps.administration.models import CompanySubscription, IndividualSubscription
from django.contrib import admin


@admin.register(CompanySubscription)
class CompanyAccountManagementAdmin(admin.ModelAdmin):
    list_display = ('company', 'start_timestamp', 'end_timestamp', 'groups')
    search_fields = ["users__email"]
    form = CompanySubsForm

@admin.register(IndividualSubscription)
class IndividualManagementAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_timestamp', 'end_timestamp', 'groups')
    search_fields = ["users__email"]

@admin.register(AccountManagementModel)
class ReportAccountManagement(admin.ModelAdmin):
    form = AccountManagementForm
    change_list_template = "admin/client/change_list.html"
    list_filter = (IsActiveCustomFilter,)
    object_history_template = []

    search_fields = ["users__email"]  

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = IndividualSubscription.objects.all()
        return qs

    def has_module_permission(self, request):
        return request.user.is_superuser