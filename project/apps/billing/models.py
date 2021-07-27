from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class Billing(models.Model):
    expiry_date = models.DateTimeField()
    user = models.ForeignKey(get_user_model(),
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

