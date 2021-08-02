from datetime import timedelta
from django.db import models
from apps.privilege_manager.models import Group
from django.utils import timezone

# Create your models here.

class Subscription(models.Model):

    SUBSCRIPTION_TYPE = [
        ('INDIVIDUAL', 'INDIVIDUAL'),
        ('COMPANY', 'COMPANY')
    ]

    start_timestamp = models.DateTimeField(null=True, auto_now_add=True)
    end_timestamp = models.DateTimeField(null=True)
    subscription_type = models.CharField(max_length=50, choices=SUBSCRIPTION_TYPE, null=True)
    groups = models.ManyToManyField(Group, blank=True, related_name="subscription_groups")

    def is_active(self) -> bool:
        start = self.start_timestamp
        end = self.end_timestamp or timezone.now() + timedelta(days=100)
        return (end - start).days > 0
