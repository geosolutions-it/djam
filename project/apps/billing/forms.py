
from django.forms import ModelForm
from apps.billing.models import Company

from django.contrib.admin.widgets import FilteredSelectMultiple    
from django.contrib.auth import get_user_model
from django.forms import ModelForm, ModelMultipleChoiceField

class CompanyAdminForm(ModelForm):
    users = ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=FilteredSelectMultiple("users__email", is_stacked=False),
        required=False
    )

    class Meta:
        model = Company
        fields = ("company_name", "users")

    