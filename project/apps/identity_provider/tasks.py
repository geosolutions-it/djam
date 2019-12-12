import dramatiq
from django.core.mail import send_mail


@dramatiq.actor(max_retries=3)
def email_user(email, subject, message):
    send_mail(subject, message, "support@djam.com", [email])
