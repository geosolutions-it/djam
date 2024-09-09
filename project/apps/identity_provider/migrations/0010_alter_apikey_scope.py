# Generated by Django 4.2 on 2024-09-09 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity_provider', '0009_apikey_expiry_apikey_scope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='scope',
            field=models.CharField(choices=[('Management', 'management'), ('Resource', 'resource')], default='resource', max_length=50),
        ),
    ]
