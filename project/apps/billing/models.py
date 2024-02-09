from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from apps.privilege_manager.models import Group
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy as _
from apps.identity_provider.models import ApiKey


class Company(models.Model):
    company_name = models.CharField(max_length=250, null=True, blank=True)

    users = models.ManyToManyField(
        get_user_model(), blank=True, related_name="company_users"
    )

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self) -> str:
        return self.company_name


class Subscription(models.Model):

    start_timestamp = models.DateTimeField(null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)

    groups = models.ForeignKey(Group, blank=False, null=True, on_delete=models.CASCADE)

    @property
    def is_active(self) -> bool:
        start = timezone.now()
        end = self.end_timestamp or timezone.now() + timedelta(days=100)
        return end > start

    @property
    def subscription_type(self):
        pass


@receiver(post_save, sender=get_user_model())
def create_default_subscription(sender, instance, created, **kwargs):
    from apps.billing.utils import subscription_manager

    if instance.email_confirmed and settings.DEFAULT_SUBSCRIPTION_TYPE is not None:
        _, group_name = settings.DEFAULT_SUBSCRIPTION_TYPE
        try:
            sub = subscription_manager.create_individual_subscription(
                groups=Group.objects.get(name=group_name),
                users=instance,
                start_timestamp=timezone.now(),
            )
        except Exception:
            return


@receiver(post_delete, sender=Subscription)
def deactivate_api_tokens(sender, instance, using, **kwargs):
    print("Deactivating all the TOKENS for every user")
    if getattr(instance, "companysubscription", None) is not None:
        for user in instance.companysubscription.company.users.all():
            ApiKey.objects.filter(user=user).update(revoked=True)
    elif getattr(instance, "individualsubscription", None) is not None:
        ApiKey.objects.filter(user=instance.individualsubscription.user).update(
            revoked=True
        )
