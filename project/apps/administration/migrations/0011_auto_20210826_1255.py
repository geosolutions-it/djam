# Generated by Django 3.0 on 2021-08-26 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0010_auto_20210825_1122'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='individualsubscription',
            name='unique_user_per_subscription',
        ),
    ]
