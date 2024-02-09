from apps.privilege_manager.models import Group
from apps.billing.enums import SubscriptionPermissions, SubscriptionTypeEnum
from apps.administration.models import AccountManagementModel
from django import forms
from apps.billing.utils import subscription_manager


class AccountManagementForm(forms.ModelForm):
    class Meta:
        model = AccountManagementModel
        exclude = []


class CompanySubsForm(forms.ModelForm):
    groups = forms.ChoiceField(
        choices=[(x.lower(), x.lower()) for x in SubscriptionPermissions.COMPANY]
    )

    def clean(self):
        cleaned_data = super().clean()
        users = cleaned_data["company"].users.all()
        cleaned_data["groups"] = Group.objects.get(name=cleaned_data["groups"])
        if self.instance and not self.instance.pk:
            try:
                subscription_manager.can_add_new_subscription_by_user(
                    users, SubscriptionTypeEnum.COMPANY
                )
            except Exception as e:
                # TODO: add the list of the users to be checked
                raise forms.ValidationError(
                    "One of the users of the selected company, already have a COMPANY subscription. Please verify the company settings before create the subscription"
                )

        return cleaned_data


class IndividualSubsForm(forms.ModelForm):
    groups = forms.ChoiceField(
        choices=[(x.lower(), x.lower()) for x in SubscriptionPermissions.INDIVIDUAL]
    )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["groups"] = Group.objects.get(name=cleaned_data["groups"])
        if self.instance and not self.instance.pk:
            try:
                subscription_manager.can_add_new_subscription_by_user(
                    cleaned_data["user"], SubscriptionTypeEnum.INDIVIDUAL
                )
            except Exception as e:
                # TODO: add the list of the users to be checked
                raise forms.ValidationError(
                    "The selected user already have an active INDIVIDUAL subscription."
                )

        return cleaned_data
