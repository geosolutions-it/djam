# Generated by Django 4.2 on 2024-05-06 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "privilege_manager",
            "0007_team_delete_group_alter_openidloginprevention_groups",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="openidloginprevention", old_name="groups", new_name="teams",
        ),
    ]
