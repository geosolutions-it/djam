# Generated by Django 3.0 on 2021-08-04 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0009_auto_20210802_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='end_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]