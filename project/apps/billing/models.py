from datetime import timedelta
from apps.billing.enums import SubscriptionTypeEnum
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from apps.privilege_manager.models import Group
from django.utils import timezone
from django.db.models.signals import m2m_changed

# Create your models here.


class Subscription(models.Model):

    SUBSCRIPTION_TYPE = [("INDIVIDUAL", "INDIVIDUAL"), ("COMPANY", "COMPANY")]

    company_name = models.CharField(max_length=250, null=True, blank=True)
    start_timestamp = models.DateTimeField(null=True, auto_now_add=True, editable=True)
    end_timestamp = models.DateTimeField(null=True)
    subscription_type = models.CharField(
        max_length=50, choices=SUBSCRIPTION_TYPE, null=True
    )
    groups = models.ManyToManyField(
        Group, blank=True, related_name="subscription_groups"
    )
    users = models.ManyToManyField(
        get_user_model(), blank=True, related_name="subscription_users"
    )

    def is_active(self) -> bool:
        start = self.start_timestamp
        end = self.end_timestamp or timezone.now() + timedelta(days=100)
        return (end - start).days > 0
