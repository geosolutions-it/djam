from apps.billing.enums import SubscriptionPermissions
from apps.billing.models import Company, Subscription
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractBaseModel(models.Model):
    class Meta:
        abstract = True

class AccountManagementModel(AbstractBaseModel):

    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        get_user_model(), blank=True, related_name="accountmodel_users", on_delete=models.CASCADE
    )
    company = models.ForeignKey(Company, max_length=250, blank=True, null=True, on_delete=models.CASCADE)

    subscription_plan = models.CharField(max_length=250, choices=[(x, x) for x in SubscriptionPermissions.ALL])
    class Meta:
        verbose_name = _("Account Management")
        verbose_name_plural = _("Account Management")
        managed = False


class CompanySubscription(Subscription):
    company = models.ForeignKey(Company, max_length=250, blank=False, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.company.company_name
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company'], name="unique_company_per_subscription")
        ]

    @property
    def subscription_type(self):
        return "company"

class IndividualSubscription(Subscription):
    user = models.ForeignKey(
        get_user_model(), blank=False, related_name="individual_users", on_delete=models.CASCADE
    )
    
    def __str__(self) -> str:
        return self.user.email

    @property
    def subscription_type(self):
        return "individual"