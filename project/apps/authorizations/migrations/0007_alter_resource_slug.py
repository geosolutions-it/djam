# Generated by Django 4.2 on 2024-06-03 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorizations", "0006_remove_resource_name_remove_resource_path_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resource",
            name="slug",
            field=models.SlugField(unique=True, verbose_name="Slug"),
        ),
    ]
