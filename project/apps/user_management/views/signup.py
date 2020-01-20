import logging

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from apps.user_management.forms import UMUserCreationForm
from apps.user_management.tasks import send_activation_email, send_staff_notification_email
from apps.user_management.utils import generate_activation_link

logger = logging.getLogger(__name__)


class SignupView(View):

    def get(self, request):
        form = UMUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UMUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # notify admin
            if settings.IP_USER_REGISTRATION_NOTIFICATION:
                notification_task = send_staff_notification_email.send(f'New user registerd with username: "{user.username}" and email: "{user.email}"')
                logger.info(
                    f'Djam USER_REGISTRATION_NOTIFICATION staff members notification email queued to be sent. '
                    f'Dramatiq message_id: {notification_task.message_id}'
                )

            # compose activation link
            activation_url = generate_activation_link(user.username, request)

            if activation_url is None:
                user.delete()
                return render(
                    request,
                    'simple_message.html',
                    context={'error': f'Could not generate activation URL.<br> Please try registering <a href="{request.get_full_path()}">again</a>!'}
                )

            # send activation message
            activation_task = send_activation_email.send(user.email, activation_url)
            logger.info(f'Activation email queued to be sent to "{user.email}". Dramatiq message_id: {activation_task.message_id}')

            return redirect(reverse('activation_msg_sent'))
        else:
            return render(request, 'signup.html', {'form': form, 'errors': form.errors})
