# Generated by Django 3.0 on 2020-01-23 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('privilege_manager', '0002_auto_20200121_0811'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='user',
            new_name='users',
        ),
    ]
