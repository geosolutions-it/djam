# Generated by Django 4.2 on 2024-05-13 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorizations", "0003_resource_type_resource_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="path",
            field=models.CharField(blank=True, null=True, verbose_name="path"),
        ),
    ]