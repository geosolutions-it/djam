from apps.administration.models import AccountManagementModel, CompanyManagementModel, IndividualManagementModel
from django import forms


class AccountManagementForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # We can't assume that kwargs['initial'] exists! 
        if 'instance' in kwargs and kwargs.get('instance'):
            instance = kwargs.get('instance')
            kwargs['initial'] = {
                "start_timestamp": instance.start_timestamp,
                "end_timestamp": instance.end_timestamp,
                "subscription_plan": instance.groups.first().name.upper(),
                "company": instance.company,
                "user": instance.users,
            }

        if args:
            new_args = args[0].copy()
            for el in ['subscription_plan']:
                if el not in args[0]:
                    new_args[el] = kwargs['initial'].get(el)
            args = new_args, args[1]

        super(AccountManagementForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs.get('instance'):
            self.fields.get('subscription_plan').widget.attrs['disabled'] = True

    class Meta:
        model = AccountManagementModel
        exclude = []


class CompanyManagementForm(AccountManagementForm):
    class Meta:
        model = CompanyManagementModel
        exclude = []

class IndividualManagementForm(AccountManagementForm):
    class Meta:
        model = IndividualManagementModel
        exclude = []
