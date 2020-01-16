import dramatiq
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.contrib.auth import get_user_model


@dramatiq.actor(max_retries=3)
def send_activation_email(email, activation_url, sender='support@djam.com', subject="Activate Your Account"):

    msg_html = render_to_string(
        'activation_email.html',
        {
            'activation_url': activation_url,
            # TODO: change this once any server is deployed
            'greeting_url': 'https://image.flaticon.com/icons/png/512/774/774502.png',
            'logo_url': 'https://mapstand-frontend-prod.s3-eu-west-2.amazonaws.com/images/logo-inverted.png',
        }
    )

    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, to=[email])
    msg.content_subtype = "html"
    return msg.send()


@dramatiq.actor(max_retries=3)
def send_staff_notification_email(msg, sender='support@djam.com', subject="Djam administration notification"):

    UserModel = get_user_model()
    staff_members = UserModel.objects.all().filter(is_staff=True)

    msg = EmailMessage(subject=subject, body=msg, from_email=sender, to=[staff_member.email for staff_member in staff_members])
    return msg.send()
