import logging
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, AuthenticationForm
from django.forms import ModelForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .tasks import send_multi_alternatives_mail


logger = logging.getLogger(__name__)


class UMUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    consent = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'consent',)


class UMAdminUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', )


class UMAdminUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        field_classes = {}


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


class UserAccountForm(ModelForm):
    last_name = forms.CharField(max_length=30, required=False)
    first_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', )


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

    def save(
            self,
            domain_override=None,
            subject_template_name='registration/password_reset_subject.txt',
            email_template_name='registration/password_reset_email.html',
            use_https=False,
            token_generator=default_token_generator,
            from_email=None,
            request=None,
            html_email_template_name=None,
            extra_email_context=None
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user's email, which is registered in the database (case-sensitive).
        """

        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user.email, html_email_template_name=html_email_template_name,
            )


class UMAuthenticationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

        if not user.email_confirmed:
            raise forms.ValidationError(
                # Error message cannot be added to self.error_messages, as usage of reverse() function at a class definition level causes
                # in this case form import error.
                _(
                    f'Please confirm your email before continuation.'
                    f'Do you want to <a href="{reverse("resend_verification_email")}">re-send activation email</a>?'
                ),
                code='email_not_confirmed',
            )
