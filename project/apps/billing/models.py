from django.db import models
from apps.privilege_manager.models import Group
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
