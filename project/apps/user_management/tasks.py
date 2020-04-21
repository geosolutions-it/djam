import typing
import dramatiq
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.contrib.auth import get_user_model


@dramatiq.actor(max_retries=3)
def send_activation_email(email, activation_url, sender=settings.DEFAULT_FROM_EMAIL, subject="Activate Your Account"):
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    msg_html = render_to_string(
        'user_management/activation_email.html',
        {
            'activation_url': activation_url,
            # TODO: change this once any server is deployed
            'logo_url': 'https://mapstand-frontend-prod.s3-eu-west-2.amazonaws.com/images/logo-inverted.png',
        }
    )

    msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, to=[email])
    msg.content_subtype = "html"
    return msg.send()


@dramatiq.actor(max_retries=3)
def send_user_notification_email(msg: str, receivers: typing.List, sender=settings.DEFAULT_FROM_EMAIL, subject="Djam notification"):
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    msg = EmailMessage(subject=subject, body=msg, from_email=sender, to=receivers)
    return msg.send()


@dramatiq.actor(max_retries=3)
def send_staff_notification_email(msg, sender=settings.DEFAULT_FROM_EMAIL, subject="Djam administration notification"):
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    UserModel = get_user_model()
    staff_members = UserModel.objects.all().filter(is_staff=True)

    msg = EmailMessage(subject=subject, body=msg, from_email=sender, to=[staff_member.email for staff_member in staff_members])
    return msg.send()


@dramatiq.actor(max_retries=3)
def send_multi_alternatives_mail(
        subject_template_name: str,
        email_template_name: str,
        context: dict,
        from_email: str,
        to_email: str,
        html_email_template_name=None
):
    """
    Function sending EmailMultiAlternatives
    """

    subject = render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])

    if html_email_template_name is not None:
        html_email = render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()
    print(email_template_name)
    print(html_email_template_name)
