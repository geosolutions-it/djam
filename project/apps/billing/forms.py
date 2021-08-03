from apps.billing.enums import SubscriptionTypeEnum
from django import forms
from apps.billing.models import Subscription


class SubscriptionForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        if not self.has_changed():
            return cleaned_data
        sub_type = cleaned_data.get("subscription_type", '').upper()

        from apps.billing.utils import SubscriptionManager
        manager = SubscriptionManager()
        if sub_type == "INDIVIDUAL":
            manager.validate_subscription(getattr(SubscriptionTypeEnum, "INDIVIDUAL"), cleaned_data.get("groups"), cleaned_data.get("users"))
        elif sub_type == "COMPANY":
            manager.validate_subscription(getattr(SubscriptionTypeEnum, "COMPANY"), cleaned_data.get("groups"), cleaned_data.get("users"))

        return cleaned_data

    class Meta:
        model = Subscription
        exclude = ['id']
