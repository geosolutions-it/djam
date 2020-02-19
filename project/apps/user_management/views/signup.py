import logging

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from apps.user_management.forms import UMUserCreationForm
from apps.user_management.tasks import send_activation_email, send_staff_notification_email
from apps.user_management.utils import generate_activation_link
from django.contrib.sites.shortcuts import get_current_site

logger = logging.getLogger(__name__)


class SignupView(View):

    def get(self, request):
        form = UMUserCreationForm()
        return render(request, 'user_management/signup.html', {'form': form})

    def post(self, request):
        form = UMUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            if not settings.REGISTRATION_MODERATION:
                user.is_active = True
                user.save()

            # compose activation link
            activation_url = generate_activation_link(user.username, request)

            if activation_url is None:
                user.delete()
                return render(
                    request,
                    'user_management/simple_message.html',
                    context={'error': f'Could not generate activation URL.<br> Please try registering <a href="{request.get_full_path()}">again</a>!'}
                )

            if settings.REGISTRATION_EMAIL_CONFIRMATION:
                # send activation message
                activation_task = send_activation_email.send(user.email, activation_url)
                logger.info(f'Activation email queued to be sent to "{user.email}". Dramatiq message_id: {activation_task.message_id}')

                return redirect(reverse('activation_msg_sent'))
            elif settings.REGISTRATION_MODERATION:

                # send activation request to staff members to activate user's account
                request_schema = 'https://' if request.is_secure() else 'http://'

                notification_task = send_staff_notification_email.send(
                    f'User with email: "{user.email}" has requested an account activation. '
                    f'You can enable access by setting the user as active on the admin section: '
                    f'{request_schema + get_current_site(request).domain}/admin/user_management/user/{user.id}'
                )
                logger.info(
                    f'Djam REGISTRATION_MODERATION email notification to staff members queued to be sent.'
                    f'Dramatiq message_id: {notification_task.message_id}'
                )

                return render(
                    request,
                    'user_management/simple_message.html',
                    context={
                        'message': "Your registration request was sent to our staff.<br>"
                                   "We'll notify you as soon as your request is approved by our staff :)"
                    },
                )
            else:
                return render(
                    request,
                    'user_management/simple_message.html',
                    context={
                        'message': f'Congrats!<br>You have successfully<br>activated your account :)<br>'
                                   f'From now on you can <a href={reverse("login")}>log in</a>.'
                    },
                )
        else:
            return render(request, 'user_management/signup.html', {'form': form, 'errors': form.errors})
