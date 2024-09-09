# Generated by Django 4.2 on 2024-09-09 11:02

import apps.identity_provider.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity_provider', '0008_remove_apikey_wms_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='expiry',
            field=models.DateTimeField(default=apps.identity_provider.models.default_expiration_date),
        ),
        migrations.AddField(
            model_name='apikey',
            name='scope',
            field=models.CharField(choices=[('resource', '1'), ('management', '2')], default='resource', max_length=50),
        ),
    ]
