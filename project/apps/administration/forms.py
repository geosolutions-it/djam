from apps.administration.models import AccountManagementModel
from django import forms


class AccountManagementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # We can't assume that kwargs['initial'] exists! 
        if 'instance' in kwargs:
            instance = kwargs.get('instance')
            kwargs['initial'] = {
                "company_name": instance.company_name,
                "end_timestamp": instance.end_timestamp,
                "subscription_type": instance.subscription_type,
                "subscription_plan": instance.groups.first().name.upper(),
                "user": instance.users.first().username,
                "api_token": instance.users.first().apikey_set.filter(revoked=False).first().key
            }

        super(AccountManagementForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AccountManagementModel
        exclude = []
