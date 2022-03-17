from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelMultipleChoiceField


from apps.billing.models import Company


class CompanyAdminForm(ModelForm):
    users = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=FilteredSelectMultiple("users__email", is_stacked=False),
        required=False
    )

    class Meta:
        model = Company
        fields = ("company_name", "users")

    def clean(self):
        invalid_users = []
        users = self.cleaned_data['users']
        for user in users:
            if not user in self.instance.users.all() and user.company_users.exists():
                invalid_users.append(user.email)
        if invalid_users:
            raise ValidationError(
                f"The following users already belong to another company, Select users who are not connected to any company yet: {invalid_users}")
        super(CompanyAdminForm, self).clean()
