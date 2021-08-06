from apps.administration.forms import AccountManagementForm
from apps.privilege_manager.models import Group
from apps.billing.utils import subscription_manager
from apps.administration.admin_filters import IsActiveCustomFilter, SubscriptionTypeFilter
from apps.identity_provider.models import ApiKey
from apps.administration.models import AccountManagementModel
from apps.billing.models import Subscription
from django.contrib import admin, messages
from django.contrib.auth import get_user_model


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
        try:
            messages.set_level(request, messages.SUCCESS)
            if not change:        
                group = Group.objects.get(name=obj.subscription_plan.lower())
                user = get_user_model().objects.get(username=obj.user)
                if obj.subscription_type == 'INDIVIDUAL':
                    subscription_manager.create_individual_subscription(groups=group, users=user)
                else:
                    subscription_manager.create_company_subscription(groups=group, users=user)
            else:
                print("Updating :)")
            
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
