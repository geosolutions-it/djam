from django.urls import path, include
from apps.user_management.views.signup import SignupView
from apps.user_management.views.email_confirmation import EmailConfirmationView, EmailConfirmationSentView, ResendVerificationEmailView


urlpatterns = [
    path(r'accounts/', include('django.contrib.auth.urls')),
    path(r'user/register/', SignupView.as_view(), name='register'),
    path(r'user/activation_msg_sent/', EmailConfirmationSentView.as_view(), name='activation_msg_sent'),
    path(r'user/<uuid:user_uuid>/email_confirmation/', EmailConfirmationView.as_view(), name='email_confirmation'),
    path(r'user/resend_activation_email/', ResendVerificationEmailView.as_view(), name='resend_verification_email'),
]
