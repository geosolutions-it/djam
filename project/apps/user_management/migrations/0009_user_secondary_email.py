# Generated by Django 3.0 on 2021-04-02 08:16

import apps.user_management.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user_management", "0008_auto_20200630_1324"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="secondary_email",
            field=apps.user_management.models.CaseInsensitiveEmailField(
                blank=True,
                max_length=254,
                null=True,
                verbose_name="secondary email address",
            ),
        ),
    ]
