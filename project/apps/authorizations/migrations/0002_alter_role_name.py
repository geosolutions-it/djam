# Generated by Django 4.2 on 2024-05-09 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorizations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="role",
            name="name",
            field=models.CharField(unique=True, verbose_name="Name"),
        ),
    ]
