from django.urls import path, include
from .views.signup_view import SignupView
from .views.email_confirmation_view import EmailConfirmationView
from .views.email_confirmation_sent_view import EmailConfirmationSentView


urlpatterns = [
    path(r'accounts/', include('django.contrib.auth.urls')),
    path(r'register/', SignupView.as_view(), name='register'),
    path(r'activation_msg_sent/', EmailConfirmationSentView.as_view(), name='activation_msg_sent'),
    path(r'user/<uuid:user_uuid>/email_confirmation/', EmailConfirmationView.as_view(), name='email_confirmation'),
]
