from apps.administration.forms import AccountManagementForm, CompanyManagementForm, IndividualManagementForm
from apps.privilege_manager.models import Group
from apps.billing.utils import subscription_manager
from apps.administration.admin_filters import (
    IsActiveCustomFilter,
    SubscriptionTypeFilter,
)
from apps.administration.models import CompanyManagementModel, IndividualManagementModel, AccountManagementModel
from apps.billing.models import Subscription
from django.contrib import admin, messages

class AccountManagementAdmin(admin.ModelAdmin):
  
    def get_queryset(self, request):
        qs = Subscription.objects.all()
        return qs

    def has_module_permission(self, request):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        # dividing flows based if is a new subscription or an update
        try:
            messages.set_level(request, messages.SUCCESS)
            if not change:
                group = Group.objects.get(name=obj.subscription_plan.lower())
                user = form.cleaned_data.get("user")
                if obj.subscription_plan != "ENTERPRISE":
                    subscription_manager.create_individual_subscription(
                        groups=group, users=user
                    )
                else:
                    new_sub = subscription_manager.create_company_subscription(
                        groups=group, users=user
                    )
                    obj.id = new_sub.id

            else:
                updated_value, _ = subscription_manager.update_subscription(
                    subscription=obj, users=form.cleaned_data.get("user"),
                    company_name=form.cleaned_data.get("company_name"),
                    end_timestamp=form.cleaned_data.get("end_timestamp"),
                    start_timestamp=form.cleaned_data.get("start_timestamp")
                )
                new_user = updated_value.get('new_users', [])
                not_added = updated_value.get('user_already_present', [])
                user_to_remove = updated_value.get('user_to_remove', [])
                # Successfuly message for the users added to the subscription
                if new_user:
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
                if user_to_remove:
                    messages.warning(
                        request,
                        f"Users removed: {', '.join([u.username for u in user_to_remove])}",
                    )

        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e.args[0])

    def save_related(self, request, form, formsets, change):
        pass

    def construct_change_message(self, request, form, formsets, add=False):
        change_message = []
        if add:
             change_message.append({'added': []})
        else:
             change_message.append({'updated': []})
        return change_message        


@admin.register(CompanyManagementModel)
class CompanyAccountManagementAdmin(AccountManagementAdmin):
    form = CompanyManagementForm
    search_fields = ["users__email"]

@admin.register(IndividualManagementModel)
class IndividualManagementAdmin(AccountManagementAdmin):
    form = IndividualManagementForm
    search_fields = ["users__email"]

@admin.register(AccountManagementModel)
class ReportAccountManagement(AccountManagementAdmin):
    form = AccountManagementForm
    change_list_template = "admin/client/change_list.html"
    list_filter = (IsActiveCustomFilter, SubscriptionTypeFilter)
    object_history_template = []

    search_fields = ["users__email"]  

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
