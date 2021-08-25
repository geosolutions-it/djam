from apps.billing.enums import SubscriptionTypeEnum
from apps.administration.models import AccountManagementModel
from django import forms
from apps.billing.utils import subscription_manager


class AccountManagementForm(forms.ModelForm):
    class Meta:
        model = AccountManagementModel
        exclude = []

class CompanySubsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        users = cleaned_data['company'].users.all()
        try:
            subscription_manager.can_add_new_subscription_by_user(users, SubscriptionTypeEnum.COMPANY)
        except Exception as e:
            # TODO: add the list of the users to be checked
            raise forms.ValidationError("One of the users of the selected company, already have a COMPANY subscription. Please verify the company settings before create the subscription")

        return cleaned_data