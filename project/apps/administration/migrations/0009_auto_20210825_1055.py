# Generated by Django 3.0 on 2021-08-25 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0008_auto_20210825_1015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companysubscription',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='individualsubscription',
            name='groups',
        ),
    ]
