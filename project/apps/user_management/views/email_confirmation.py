import logging
from datetime import timedelta

from django.views import View
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from apps.user_management.models import UserActivationCode
from apps.user_management.tasks import send_activation_email, send_staff_notification_email
from apps.user_management.utils import generate_activation_link
from apps.user_management.forms import ResendActivationEmailForm

logger = logging.getLogger(__name__)


class EmailConfirmationSentView(View):

    def get(self, request):
        return render(request, 'user_management/simple_message.html', context={'message': 'Please confirm your email address <br> to complete registration.'})


class EmailConfirmationView(View):

    def get(self, request, user_uuid, *args, **kwargs):
        activation_code = request.GET.get('activation_code')

        try:
            user = get_user_model().objects.get(uuid=user_uuid)
        except ObjectDoesNotExist:
            logger.error(f'Email Confirmation View: No registered user found with user_uuid: {user_uuid}')
            return self.render_error(request, 'Whoops.. Something went wrong.')

        if user.email_confirmed:
            logging.info(f'Email Confirmation View: The user has already confirmed the email "{user.email}"')
            return self.render_error(request, 'Whoops.. Your email is already confirmed.')

        user_activation_code = UserActivationCode.objects.filter(activation_code=activation_code).first()
        if user_activation_code is None:
            logging.error(f'Email Confirmation View: User Activation Code not found: {activation_code}')
            return self.render_error(request, f'Whoops.. Something went wrong.<br><a href="{request.build_absolute_uri(reverse("resend_verification_email"))}">Resend an activation email</a>.')

        if user_activation_code.user.id != user.id:
            logging.error(f'Email Confirmation View: User activation code mismatch for user: {user.email}')
            return self.render_error(request, f'Whoops.. Something went wrong.<br><a href="{request.build_absolute_uri(reverse("resend_verification_email"))}">Resend an activation email</a>.')

        code_expired = timedelta(hours=settings.IP_ACTIVATION_CODE_EXPIRATION_HOURS) < (timezone.now() - user_activation_code.creation_date)

        if code_expired:
            logging.error(f'Email Confirmation View: User activation code expired for user: {user.email}')
            return self.render_error(request, f'Whoops... Your activation code has expired.<br><a href="{request.build_absolute_uri(reverse("resend_verification_email"))}">Resend an activation email</a>.')

        user_activation_code.user.email_confirmed = True
        user_activation_code.user.save()

        user_activation_code.delete()

        # TODO: add the User to default Permission Group

        # notify staff users
        if settings.IP_USER_EMAIL_CONFIRMATION_NOTIFICATION:
            notification_task = send_staff_notification_email.send(
                f'User with username: "{user.username}" and email: "{user.email}" has verified the email.'
            )
            logger.info(
                f'Djam USER_EMAIL_CONFIRMATION_NOTIFICATION staff members notification email queued to be sent. '
                f'Dramatiq message_id: {notification_task.message_id}'
            )

        return render(
            request,
            'user_management/simple_message.html',
            context={'message': 'Congrats!<br>You have successfully<br>activated your account :)'},
        )

    def render_error(self, request, error):
        return render(
            request,
            'user_management/simple_message.html',
            context={'error': error}
        )


class ResendVerificationEmailView(View):

    def get(self, request):
        form = ResendActivationEmailForm()
        return render(request, 'user_management/signup_resend_activation_email.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ResendActivationEmailForm(request.POST)
        logger.info(f'Resend Email Verification View: User with email "{form.data["email"]}" requested resending activation message.')

        if form.is_valid():
            user_email = form.cleaned_data['email']
            user = get_user_model().objects.filter(email=user_email).first()

            if user is None:
                logger.error(f'Resend Email Verification View: No registered user found with email: {user_email}')

                return render(request, 'user_management/signup_resend_activation_email.html', {'form': form})

            if user.email_confirmed:
                logging.info(f'Resend Email Verification View: The user has already confirmed the email "{user.email}"')
                return self.render_error(request, 'Your email is already confirmed.<br> No need for resending activation email :)')

            # compose activation link
            activation_url = generate_activation_link(user.username, request)
            # re-send activation message
            activation_task = send_activation_email.send(user.email, activation_url)
            logger.info(
                f'Resend Email Verification View: Resend of activation email queued to be sent to "{user.email}". '
                f'Dramatiq message_id: {activation_task.message_id}'
            )

            return redirect(reverse('activation_msg_sent'))

        else:
            return render(request, 'user_management/signup_resend_activation_email.html', {'form': form})

    def render_error(self, request, error):
        return render(
            request,
            'user_management/simple_message.html',
            context={'error': error}
        )
