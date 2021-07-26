from django.contrib.auth import get_user_model
import django.http
from django.shortcuts import redirect
from django.urls.conf import path
from apps.administration.models import AccountManagementModel
from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.main import ChangeList
# Register your models here.

@admin.register(AccountManagementModel)
class AccountManagementAdmin(admin.ModelAdmin):
    change_list_template = 'admin/client/change_list.html'

    object_history_template = []

    list_display = [
        "id",
        "email",
        "company_name",
    ]

    search_fields = ['username']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upgrade/', self.account_upgrade, name="account_upgrade"),
            path('downgrade/', self.account_downgrade, name="account_downgrade")
        ]
        return my_urls + urls

    def get_queryset(self, request):
        qs = get_user_model().objects.all().order_by('id')
        return qs

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj, **kwargs)

    def get_actions(self, request):
        return {}

    def has_add_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_superuser

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super(AccountManagementAdmin, self).changelist_view(request, extra_context=extra_context)

    def account_upgrade(self, request):
        self.message_user(request, "The Selected account has been upgraded", messages.SUCCESS)
        return redirect("..")

    def account_downgrade(self, request):
        self.message_user(request, "The Selected account has been downgraded", messages.SUCCESS)
        return redirect("..")