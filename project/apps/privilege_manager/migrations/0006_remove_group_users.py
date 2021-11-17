# Generated by Django 3.0 on 2021-11-16 15:26

from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.db import migrations
from apps.billing.models import Company
from apps.billing.utils import SubscriptionException, subscription_manager as sub_man
from apps.billing.enums import SubscriptionTypeEnum
from apps.administration.models import IndividualSubscription
from apps.privilege_manager.models import Group


def create_individual_subscriptions(apps, schema_editor):
    Groups = apps.get_model("privilege_manager", "Group")
    for group in Groups.objects.filter(name__in=['free', 'pro']).order_by('id'):
        for user in group.users.filter(email_confirmed=True):
            _user_instance = get_user_model().objects.filter(id=user.id).first()
            _group_instance = Group.objects.filter(id=group.id).first()
            try:
                if sub_man.can_add_new_subscription_by_user(_user_instance, SubscriptionTypeEnum.INDIVIDUAL):
                    sub_man.create_individual_subscription(
                        _group_instance,
                        _user_instance,
                        start_timestamp=datetime.utcnow()
                    )
            except SubscriptionException:
                IndividualSubscription.objects.filter(user=_user_instance).update(groups=group)
                pass

def create_company_subscriptions(apps, schema_editor):
    Groups = apps.get_model("privilege_manager", "Group")    
    for group in Groups.objects.filter(name__in=['enterprise']).order_by('id'):
        for user in group.users.filter(email_confirmed=True):
            _user_instance = get_user_model().objects.filter(id=user.id).first()
            _group_instance = Group.objects.filter(id=group.id).first()          
            try:
                if sub_man.can_add_new_subscription_by_user(_user_instance, SubscriptionTypeEnum.COMPANY):
                    _company = Company.objects.filter(users=_user_instance)
                    if _company.exists():
                        sub_man.create_company_subscription(
                            _group_instance,
                            _company.get(),
                            start_timestamp=datetime.utcnow(),
                            end_timestamp=datetime.utcnow()
                        )
            except SubscriptionException:
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('privilege_manager', '0005_openidloginprevention'),
        ('billing', '0016_auto_20210826_1255')
    ]

    operations = [
        migrations.RunPython(create_individual_subscriptions),
        migrations.RunPython(create_company_subscriptions),
        migrations.RemoveField(
            model_name='group',
            name='users',
        ),
    ]

