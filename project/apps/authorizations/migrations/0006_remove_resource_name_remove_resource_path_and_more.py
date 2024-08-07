# Generated by Django 4.2 on 2024-06-03 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authorizations", "0005_alter_resource_path"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resource",
            name="name",
        ),
        migrations.RemoveField(
            model_name="resource",
            name="path",
        ),
        migrations.AddField(
            model_name="resource",
            name="slug",
            field=models.SlugField(verbose_name="Slug"),
            preserve_default=False,
        ),
    ]
