# Generated by Django 3.0 on 2020-02-18 14:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('identity_provider', '0004_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='user',
            field=models.ForeignKey(help_text="API key will have the same privilege groups as it's owner.", on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
