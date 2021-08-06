from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from apps.administration.forms import AccountManagementForm
from apps.privilege_manager.models import Group
from apps.billing.utils import subscription_manager
from apps.administration.admin_filters import (
    IsActiveCustomFilter,
    SubscriptionTypeFilter,
)
from apps.identity_provider.models import ApiKey
from apps.administration.models import AccountManagementModel
from apps.billing.models import Subscription
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.db import transaction


@admin.register(AccountManagementModel)
class AccountManagementAdmin(admin.ModelAdmin):
    form = AccountManagementForm

    change_list_template = "admin/client/change_list.html"
    list_filter = (IsActiveCustomFilter, SubscriptionTypeFilter)
    object_history_template = []

    search_fields = ["users__email"]

    def get_queryset(self, request):
        qs = Subscription.objects.all()
        return qs

    def has_module_permission(self, request):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        # dividing flows based if is a new subscription or an update
        with transaction.atomic():
            try:
                messages.set_level(request, messages.SUCCESS)
                if not change:
                    group = Group.objects.get(name=obj.subscription_plan.lower())
                    user = get_user_model().objects.get(username=obj.user)
                    if obj.subscription_type == "INDIVIDUAL":
                        subscription_manager.create_individual_subscription(
                            groups=group, users=user
                        )
                    else:
                        subscription_manager.create_company_subscription(
                            groups=group, users=user
                        )
                else:
                    new_user = []
                    not_added = []
                    user_to_remove = []
                    group = Group.objects.get(
                        name=form.cleaned_data.get("subscription_plan").lower()
                    )
                    for user in form.cleaned_data.get("user"):
                        # check if the user selected is already associated with the subscription
                        if obj.users.filter(username=user).exists():
                            # if yes, we skip it
                            continue
                        else:
                            # if is not already assigned to the subscription, we check if a new subscription can be added for the user
                            can_be_added = (
                                subscription_manager.can_add_new_subscription_by_user(
                                    user=user,
                                    sub_type=form.cleaned_data.get("subscription_type"),
                                )
                            )
                            if can_be_added:
                                new_user.append(user)
                            else:
                                not_added.append(user)
                    # Successfuly message for the users added to the subscription
                    if new_user:
                        obj.users.add(*new_user)
                        messages.success(
                            request,
                            f"New users added to the subscription: {', '.join([u.username for u in new_user])}",
                        )
                    # Error message for the users NOT added to the subscription
                    if not_added:
                        messages.error(
                            request,
                            f"The following users cannot be added to the selected subscription: {', '.join([u.username for u in not_added])}"
                        )
                    
                    # Warning message for the users that has been removed from the subscription:
                    usernames = [x.username for x in form.cleaned_data.get("user")]
                    for usr in obj.users.all():
                        if usr.username not in usernames:
                            user_to_remove.append(usr)
                    if user_to_remove:
                        obj.users.remove(*user_to_remove)
                        messages.warning(
                            request,
                            f"Users removed: {', '.join([u.username for u in user_to_remove])}",
                        )

            except Exception as e:
                messages.set_level(request, messages.ERROR)
                messages.error(request, e.args[0])

    @staticmethod
    def _delete_apikey(user):
        user_token = ApiKey.objects.filter(user=user)
        if user_token.exists():
            user_token.delete()

    @staticmethod
    def _end_billing(user):
        billing = Subscription.objects.filter(user=user)
        if billing.exists():
            billing.first().delete()
