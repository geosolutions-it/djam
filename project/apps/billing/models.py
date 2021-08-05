from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from apps.privilege_manager.models import Group
from django.utils import timezone
from django.db.models.signals import post_save

# Create your models here.


class Subscription(models.Model):

    SUBSCRIPTION_TYPE = [("INDIVIDUAL", "INDIVIDUAL"), ("COMPANY", "COMPANY")]

    company_name = models.CharField(max_length=250, null=True, blank=True)
    start_timestamp = models.DateTimeField(null=True, auto_now_add=True, editable=True)
    end_timestamp = models.DateTimeField(null=True, blank=True)
    subscription_type = models.CharField(
        max_length=50, choices=SUBSCRIPTION_TYPE, null=True
    )
    groups = models.ManyToManyField(
        Group, blank=True, related_name="subscription_groups"
    )
    users = models.ManyToManyField(
        get_user_model(), blank=True, related_name="subscription_users",
    )

    @property
    def is_active(self) -> bool:
        start = self.start_timestamp
        end = self.end_timestamp or timezone.now() + timedelta(days=100)
        return (end - start).days > 0


@receiver(post_save, sender=get_user_model())
def create_default_subscription(sender, instance, created, **kwargs):
    from apps.billing.utils import subscription_manager
    if created and settings.DEFAULT_SUBSCRIPTION_TYPE is not None:
        _, group_name = settings.DEFAULT_SUBSCRIPTION_TYPE
        try:
            sub = subscription_manager.create_individual_subscription(
                groups=Group.objects.get(name=group_name),
                users=instance
            )
        except models.ObjectDoesNotExist:
            return
