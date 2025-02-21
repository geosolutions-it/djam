from django.urls import path, re_path
from apps.user_management.views.account_page import (
    AccountDashboard,
    UMLoginView,
)
from django.contrib.auth import views as auth_views

from apps.user_management.views.password_change import CustomPasswordChangeView
from apps.user_management.views.signup import SignupView
from apps.user_management.forms import (
    UMPasswordResetForm,
    UMAuthenticationForm,
    CustomChangePasswordForm,
)
from apps.user_management.views.email_confirmation import (
    EmailConfirmationView,
    EmailConfirmationSentView,
    ResendVerificationEmailView,
)


urlpatterns = [

    # ---- django.contrib.auth.urls.views ----
    path(
        "accounts/login/",
        UMLoginView.as_view(form_class=UMAuthenticationForm),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path(
        "accounts/password_change/",
        CustomPasswordChangeView.as_view(
            template_name="account/password_change_form.html",
            form_class=CustomChangePasswordForm,
        ),
        name="password_change",
    ),
    path(
        "accounts/password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="account/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(form_class=UMPasswordResetForm),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # ---- end of: django.contrib.auth.urls.views ----
    path(r"user/register/", SignupView.as_view(), name="register"),
    re_path(
        r"user/account/edit/(?P<id>\w+)/",
        AccountDashboard.as_view(),
        name="user_account_edit",
    ),
    # First release views using AccountDashboard as simpler until more profile features added then use the below commented out views
    path(r"user/account/", AccountDashboard.as_view(), name="user_account"),
    re_path(
        r"user/account/(?P<id>\w+)/", AccountDashboard.as_view(), name="user_account"
    ),
    path(
        r"user/activation_msg_sent/",
        EmailConfirmationSentView.as_view(),
        name="activation_msg_sent",
    ),
    path(
        r"user/<uuid:user_uuid>/email_confirmation/",
        EmailConfirmationView.as_view(),
        name="email_confirmation",
    ),
    path(
        r"user/resend_activation_email/",
        ResendVerificationEmailView.as_view(),
        name="resend_verification_email",
    ),
]
