from apps.identity_provider.models import ApiKey
from apps.privilege_manager.models import Group
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls.conf import path
from apps.administration.models import AccountManagementModel
from django.contrib import admin, messages

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

    def get_actions(self, request):
        return {}

    def has_add_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_superuser

    def account_upgrade(self, request):
        if request.user.is_authenticated:
            try:
                user_obj = get_user_model().objects.filter(id=int(request.GET.get('account_id')))
                if user_obj.exists():
                    user = user_obj.first()
                    self._asign_group(user, 'enterprise')
                    self.message_user(request, "The Selected account has been upgraded", messages.SUCCESS)
                else:
                    self.message_user(request, "The Selected user is not present in the system", messages.ERROR)
            except Exception as e:
                self.message_user(request, e.args[0], messages.ERROR)
        return redirect("..")

    def account_downgrade(self, request):
        if request.user.is_authenticated:
            try:
                user_obj = get_user_model().objects.filter(id=int(request.GET.get('account_id')))
                if user_obj.exists():
                    user = user_obj.first()
                    self._delete_apikey(user)
                    self._asign_group(user, 'free')
                    self.message_user(request, "The Selected account has been downgraded", messages.SUCCESS)
                else:
                    self.message_user(request, "The Selected user is not present in the system", messages.ERROR)
            except Exception as e:
                self.message_user(request, e.args[0], messages.ERROR)
        return redirect("..")

    @staticmethod
    def _asign_group(user, group_name):
        user_group = user.group_set.all()
        if user_group.exists():
            user_group.first().users.remove(user)
        new_group = Group.objects.get(name=group_name)
        new_group.users.add(user)

    @staticmethod
    def _delete_apikey(user):
        user_token = ApiKey.objects.filter(user=user)
        if user_token.exists():
            user_token.delete()
