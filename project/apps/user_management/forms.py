import logging
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .tasks import send_multi_alternatives_mail

logger = logging.getLogger(__name__)


class UMUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', )


class UMAdminUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class UMAdminUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def clean_email(self):
        data = self.cleaned_data.get('email')

        try:
            get_user_model().objects.get(email=data)
        except ObjectDoesNotExist:
            logger.error(f'ResendActivationEmailForm: Validation error - no user found with "{data}" email')
            raise forms.ValidationError('No user found with registered email.')

        return data


class UMPasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Function sending password reset email using Dramatiq
        """
        # User object is not serializable - has to be replaced for passing arguments to Dramatiq
        user = context.pop('user')
        context['username'] = user.get_username()

        send_multi_alternatives_mail.send(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None
        )

        return
