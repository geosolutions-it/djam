# Generated by Django 3.0 on 2021-08-25 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("privilege_manager", "0005_openidloginprevention"),
        ("billing", "0011_auto_20210824_1154"),
    ]

    operations = [
        migrations.RemoveField(model_name="subscription", name="company",),
        migrations.RemoveField(model_name="subscription", name="groups",),
        migrations.RemoveField(model_name="subscription", name="subscription_type",),
        migrations.RemoveField(model_name="subscription", name="users",),
        migrations.AlterField(
            model_name="subscription",
            name="start_timestamp",
            field=models.DateTimeField(null=True),
        ),
        migrations.CreateModel(
            name="IndividualSubscription",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="individual_sub_groups",
                        to="privilege_manager.Group",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="individual_users",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CompanySubscription",
            fields=[
                (
                    "subscription_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="billing.Subscription",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        blank=True,
                        max_length=250,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="billing.Company",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="company_sub_groups",
                        to="privilege_manager.Group",
                    ),
                ),
            ],
            bases=("billing.subscription",),
        ),
    ]
