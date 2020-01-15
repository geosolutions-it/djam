import logging
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', )


class IPUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class IPUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def clean_email(self):
        data = self.cleaned_data.get('email')

        user = get_user_model().objects.filter(email=data).first()

        if user is None:
            logger.error(f'ResendActivationEmailForm: Validation error - no user found with "{data}" email')
            raise forms.ValidationError('No user found with registered email.')

        return data
