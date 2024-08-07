# Generated by Django 4.2 on 2024-05-09 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorizations", "0002_alter_role_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="type",
            field=models.CharField(
                choices=[("Upstream Service", "Upstream Service")],
                default=None,
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="resource",
            name="url",
            field=models.CharField(
                null=True, verbose_name="upstream url to be proxed to"
            ),
        ),
    ]
