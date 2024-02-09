import logging
from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordResetForm,
    AuthenticationForm,
    PasswordChangeForm,
    UsernameField,
)
from django.forms import ModelForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.forms.widgets import PasswordInput
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from django.conf import settings

from .tasks import send_multi_alternatives_mail

logger = logging.getLogger(__name__)


class UMUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(
        max_length=254, help_text="Required. Input a valid email address."
    )
    secondary_email = forms.EmailField(max_length=254, required=False)
    subscription = forms.BooleanField(required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV3())

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "secondary_email",
            "password1",
            "password2",
            "subscription",
        )


class UMAdminUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email",)


class UMAdminUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        field_classes = {}


class ResendActivationEmailForm(forms.Form):
    email = forms.EmailField(
        max_length=254, help_text="Required. Inform a valid email address."
    )

    def clean_email(self):
        data = self.cleaned_data.get("email")

        try:
            get_user_model().objects.get(email=data)
        except ObjectDoesNotExist:
            logger.error(
                f'ResendActivationEmailForm: Validation error - no user found with "{data}" email'
            )
            raise forms.ValidationError("No user found with that email!")

        return data


class FormSendEmailMixin:
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Function sending password reset email using Dramatiq
        """
        # User object is not serializable - has to be replaced for passing arguments to Dramatiq
        # TODO: change logo_url once any server is deployed
        user = context.pop("user")
        context["username"] = user.get_username()

        send_multi_alternatives_mail.send(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name,
        )


class UserAccountForm(FormSendEmailMixin, ModelForm):
    last_name = forms.CharField(max_length=30, required=False)
    first_name = forms.CharField(max_length=150, required=False)
    email = forms.CharField(max_length=150, required=False)
    secondary_email = forms.CharField(max_length=150, required=False)
    secondary_email = forms.CharField(max_length=150, required=False)
    subscription = forms.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "secondary_email", "subscription")

    def save(
        self,
        domain_override=None,
        subject_template_name="user_management/email_change_subject.txt",
        email_template_name="user_management/email_change_email_txt.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name="user_management/email_change_email.html",
        extra_email_context=None,
        logo_url="",
        commit=True,
    ):
        old_email = request.user.email
        obj = super().save(commit)
        if "email" in self.changed_data:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                "site_name": site_name,
                "domain": domain,
                "protocol": "https" if use_https else "http",
                "user": request.user,
                **(extra_email_context or {}),
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "logo_url": logo_url,
            }

            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                old_email,
                html_email_template_name=html_email_template_name,
            )
        return obj


class UMPasswordResetForm(FormSendEmailMixin, PasswordResetForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3())

    def clean(self):
        cleaned_data = super().clean()

        try:
            get_user_model().objects.get(email=cleaned_data["email"])
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                f"No user found with email: {cleaned_data['email']}"
            )

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email_txt.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name="registration/password_reset_email.html",
        extra_email_context=None,
        logo_url="",
    ):
        """
        Generate a one-use only link for resetting password and send it to the
        user's email, which is registered in the database (case-sensitive).
        """
        email_template_name = "registration/password_reset_email_txt.html"

        if not html_email_template_name:
            html_email_template_name = "registration/password_reset_email.html"

        for user in self.get_users(self.cleaned_data["email"]):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                "email": user.email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "logo_url": logo_url,
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user.email,
                html_email_template_name=html_email_template_name,
            )


class UMAdminAuthenticationForm(AdminAuthenticationForm):
    username = UsernameField(
        label="Email", widget=forms.TextInput(attrs={"autofocus": True})
    )
    error_messages = {
        "invalid_login": _(
            "Please enter a correct email address and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }


class UMAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Please enter a correct email address and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

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
                self.error_messages["inactive"], code="inactive",
            )

        if settings.REGISTRATION_EMAIL_CONFIRMATION:
            # if REGISTRATION_EMAIL_CONFIRMATION flow is active, login only users who confirmed their email
            if not user.email_confirmed:
                raise forms.ValidationError(
                    # Error message cannot be added to self.error_messages, as usage of reverse() function at a class definition level causes
                    # in this case form import error.
                    _(
                        f"Please confirm your email before continuation. "
                        f'Do you want to <a href="{reverse("resend_verification_email")}">re-send activation email</a>?'
                    ),
                    code="email_not_confirmed",
                )


class CustomChangePasswordForm(PasswordChangeForm, FormSendEmailMixin):
    old_password = forms.CharField(
        widget=PasswordInput(attrs={"placeholder": "Enter your old password"})
    )
    new_password1 = forms.CharField(
        widget=PasswordInput(attrs={"placeholder": "Enter your new password"})
    )
    new_password2 = forms.CharField(
        widget=PasswordInput(attrs={"placeholder": "Enter your new password (again)"})
    )

    def save(
        self,
        domain_override=None,
        subject_template_name="user_management/password_change_subject.txt",
        email_template_name="user_management/password_change_email_txt.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name="user_management/password_change_email.html",
        extra_email_context=None,
        logo_url="",
        commit=True,
    ):

        obj = super().save(commit)
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        context = {
            "site_name": site_name,
            "domain": domain,
            "protocol": "https" if use_https else "http",
            "user": self.user,
            **(extra_email_context or {}),
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "logo_url": logo_url,
        }

        self.send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            self.user.email,
            html_email_template_name=html_email_template_name,
        )
        return obj
