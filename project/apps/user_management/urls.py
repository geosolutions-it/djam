from django.urls import path
from django.contrib.auth import views as auth_views

from apps.user_management.views.signup import SignupView
from apps.user_management.forms import UMPasswordResetForm
from apps.user_management.views.email_confirmation import EmailConfirmationView, EmailConfirmationSentView, ResendVerificationEmailView

urlpatterns = [
    # ---- django.contrib.auth.urls.views ----

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(form_class=UMPasswordResetForm), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # ---- end of: django.contrib.auth.urls.views ----

    path(r'user/register/', SignupView.as_view(), name='register'),
    path(r'user/activation_msg_sent/', EmailConfirmationSentView.as_view(), name='activation_msg_sent'),
    path(r'user/<uuid:user_uuid>/email_confirmation/', EmailConfirmationView.as_view(), name='email_confirmation'),
    path(r'user/resend_activation_email/', ResendVerificationEmailView.as_view(), name='resend_verification_email'),
]
