import dramatiq
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


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
