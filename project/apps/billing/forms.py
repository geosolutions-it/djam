from apps.billing.enums import SubscriptionTypeEnum
from django import forms
from apps.billing.models import Subscription
import django.db.models


class SubscriptionForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        sub_type = cleaned_data.get("subscription_type", '').upper()

        from apps.billing.utils import SubscriptionManager
        manager = SubscriptionManager()
        if sub_type == "INDIVIDUAL":
            manager.validate_subscription(getattr(SubscriptionTypeEnum, "INDIVIDUAL"), cleaned_data.get("groups"))
        elif sub_type == "COMPANY":
            manager.validate_subscription(getattr(SubscriptionTypeEnum, "COMPANY"), cleaned_data.get("groups"))
        return cleaned_data

    class Meta:
        model = Subscription
        exclude = ['id']
