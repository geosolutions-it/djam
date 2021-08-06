from apps.administration.models import AccountManagementModel
from django import forms


class AccountManagementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # We can't assume that kwargs['initial'] exists! 
        if 'instance' in kwargs and kwargs.get('instance'):
            instance = kwargs.get('instance')
            kwargs['initial'] = {
                "company_name": instance.company_name,
                "end_timestamp": instance.end_timestamp,
                "subscription_type": instance.subscription_type,
                "subscription_plan": instance.groups.first().name.upper(),
                "user": instance.users.all(),
                "api_token": instance.users.first().apikey_set.filter(revoked=False).first().key
            }
        
        if args:
            new_args = args[0].copy()
            for el in ['api_token', 'subscription_type', 'subscription_plan']:
                if el not in args[0]:
                    new_args[el] = kwargs['initial'].get(el)
            args = new_args, args[1]

        super(AccountManagementForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs.get('instance'):
            self.fields.get('api_token').widget.attrs['disabled'] = True
            self.fields.get('subscription_type').widget.attrs['disabled'] = True
            self.fields.get('subscription_plan').widget.attrs['disabled'] = True

    class Meta:
        model = AccountManagementModel
        exclude = []
