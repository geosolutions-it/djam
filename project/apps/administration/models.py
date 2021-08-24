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

    class Meta:
        verbose_name = _("Account Management")
        verbose_name_plural = _("Account Management")
        managed = False

class IndividualManagementModel(AbstractBaseModel):
    def __str__(self):
        return self.subscription_plan
    
    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        get_user_model(), blank=True, related_name="accountmodel_users", on_delete=models.CASCADE
    )
    subscription_plan = models.CharField(max_length=250, choices=[('FREE', 'FREE'), ('PRO', 'PRO')])

    class Meta:
        verbose_name = _("Individual subscription")
        verbose_name_plural = _("Individual subscriptions")
        managed = False


class CompanyManagementModel(AbstractBaseModel):
    def __str__(self) -> str:
        return self.id
    
    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)
    company = models.ForeignKey(Company, max_length=250, blank=True, null=True, on_delete=models.CASCADE)
    subscription_plan = models.CharField(max_length=250, choices=[('ENTERPRISE', 'ENTERPRISE')])

    class Meta:
        verbose_name = _("Company subscription")
        verbose_name_plural = _("Company subscriptions")
        managed = False
