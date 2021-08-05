from apps.billing.enums import SubscriptionTypeEnum
from django import forms
from apps.billing.models import Subscription


class SubscriptionForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        if not self.has_changed():
            return cleaned_data
        sub_type = cleaned_data.get("subscription_type", '').upper()

        from apps.billing.utils import subscription_manager
        if 'users' in self.changed_data or 'groups' in self.changed_data:
            if sub_type == "INDIVIDUAL":
                subscription_manager.validate_subscription(getattr(SubscriptionTypeEnum, "INDIVIDUAL"), cleaned_data.get("groups"), cleaned_data.get("users"))
            elif sub_type == "COMPANY":
                subscription_manager.validate_subscription(getattr(SubscriptionTypeEnum, "COMPANY"), cleaned_data.get("groups"), cleaned_data.get("users"))

        return cleaned_data

    class Meta:
        model = Subscription
        exclude = ['id']
