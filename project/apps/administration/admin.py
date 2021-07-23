from apps.privilege_manager.models import Group
from django.contrib.auth import get_user_model
from apps.administration.models import AccountManagementModel
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Register your models here.

@admin.register(AccountManagementModel)
class AccountManagementAdmin(admin.ModelAdmin):
    change_list_template = 'admin/client/change_list.html'

    object_history_template = []

    list_display = [
        "email",
        "first_name",
        "last_name",
        "company_name",
    ]

    search_fields = ['username']

    def get_queryset(self, request):
        qs = get_user_model().objects.all()
        return qs

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)

    def get_actions(self, request):
        return {}

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_superuser

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super(AccountManagementAdmin, self).changelist_view(request, extra_context=extra_context)
