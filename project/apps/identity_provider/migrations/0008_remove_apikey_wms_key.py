# Generated by Django 4.2 on 2024-09-06 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('identity_provider', '0007_apikey_wms_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apikey',
            name='wms_key',
        ),
    ]