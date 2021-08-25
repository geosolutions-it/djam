from apps.administration.models import AccountManagementModel
from django import forms


class AccountManagementForm(forms.ModelForm):
    class Meta:
        model = AccountManagementModel
        exclude = []
