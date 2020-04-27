# Generated by Django 3.0 on 2020-02-18 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_management", "0004_user_consent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                verbose_name="active",
            ),
        ),
    ]
