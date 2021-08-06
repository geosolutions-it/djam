from datetime import datetime
from apps.billing.utils import subscription_manager
from apps.administration.admin_filters import IsActiveCustomFilter, SubscriptionTypeFilter
from apps.identity_provider.models import ApiKey
from apps.privilege_manager.models import Group
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls.conf import path
from apps.administration.models import AccountManagementModel
from apps.billing.models import Subscription
from django.contrib import admin, messages
from apps.billing.enums import SubscriptionTypeEnum

@admin.register(AccountManagementModel)
class AccountManagementAdmin(admin.ModelAdmin):
    change_list_template = "admin/client/change_list.html"
    list_filter = (IsActiveCustomFilter, SubscriptionTypeFilter)
    object_history_template = []

    search_fields = ["users__email"]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("upgrade/", self.account_upgrade, name="account_upgrade"),
            path("downgrade/", self.account_downgrade, name="account_downgrade"),
        ]
        return my_urls + urls

    def get_queryset(self, request):
        qs = Subscription.objects.all()
        return qs

    def has_module_permission(self, request):
        return request.user.is_superuser

    def account_upgrade(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            try:
                user_obj = get_user_model().objects.filter(
                    id=int(request.GET.get("account_id"))
                )
                if user_obj.exists():
                    user = user_obj.first()
                    try:
                        subscription_manager.can_add_new_subscription_by_user(user, SubscriptionTypeEnum.COMPANY)
                        self._asign_group(user, "enterprise")
                        self._start_billing(user)
                        self.message_user(
                            request,
                            "The Selected account has been upgraded",
                            messages.SUCCESS,
                        )
                    except:
                        self.message_user(
                            request,
                            "Upgrade not done, the Selected account already have a COMPANY subscription",
                            messages.ERROR
                        )
                else:
                    self.message_user(
                        request,
                        "The Selected user is not present in the system",
                        messages.ERROR,
                    )
            except Exception as e:
                self.message_user(request, e.args[0], messages.ERROR)
        return redirect("..")

    def account_downgrade(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            try:
                user_obj = get_user_model().objects.filter(
                    id=int(request.GET.get("account_id"))
                )
                if user_obj.exists():
                    try:
                        user = user_obj.first()
                        subscription_manager.can_add_new_subscription_by_user(user, SubscriptionTypeEnum.COMPANY)
                        self._delete_apikey(user)
                        self._asign_group(user, "free")
                        self._end_billing(user)
                        self.message_user(
                            request,
                            "The Selected account has been downgraded",
                            messages.SUCCESS,
                        )
                    except:
                        self.message_user(
                            request,
                            "Downgrade not done, the Selected account already have an INDIVIDUAL subscription",
                            messages.ERROR
                        )
                else:
                    self.message_user(
                        request,
                        "The Selected user is not present in the system",
                        messages.ERROR,
                    )
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

    @staticmethod
    def _start_billing(user):
        date = datetime.utcnow()
        billing, _ = Subscription.objects.get_or_create(
            user=user, defaults={"start_date": date, "expiry_date": None}
        )
        return billing

    @staticmethod
    def _end_billing(user):
        billing = Subscription.objects.filter(user=user)
        if billing.exists():
            billing.first().delete()
