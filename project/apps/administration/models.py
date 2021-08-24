from apps.billing.models import Company
from django import forms
from apps.privilege_manager.models import Group
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class AbstractBaseModel(models.Model):
    class Meta:
        abstract = True

class AccountManagementModel(AbstractBaseModel):
    SUBSCRIPTION_TYPE = [("INDIVIDUAL", "INDIVIDUAL"), ("COMPANY", "COMPANY")]

    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)
    subscription_type = models.CharField(
        max_length=50, choices=SUBSCRIPTION_TYPE, null=True
    )
  
    subscription_plan = models.CharField(max_length=250, choices=[('FREE', 'FREE'), ('ENTERPRISE', 'ENTERPRISE')])
    company = models.ForeignKey(Company, max_length=250, blank=True, null=True, on_delete=models.CASCADE,)

    user = models.ManyToManyField(
        get_user_model(), blank=True, related_name="accountmodel_users",
    )

    api_token = models.CharField(_('Api token'), max_length=250, blank=True, editable=True)

    class Meta:
        verbose_name = _("Account Management")
        verbose_name_plural = _("Account Management")
        managed = False

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
