from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from apps.privilege_manager.models import Group
from django.utils import timezone
from django.db.models.signals import post_save


class Company(models.Model):
    company_name = models.CharField(max_length=250, null=True, blank=True)

    users = models.ManyToManyField(
        get_user_model(), blank=True, related_name="company_users",
    )
    def __str__(self) -> str:
        return self.company_name


class Subscription(models.Model):

    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)

    groups = models.ForeignKey(
        Group, blank=True, null=True, on_delete=models.CASCADE
    )

    @property
    def is_active(self) -> bool:
        start = timezone.now()
        end = self.end_timestamp or timezone.now() + timedelta(days=100)
        return end > start


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
