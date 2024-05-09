# Generated by Django 4.2 on 2024-05-06 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("privilege_manager", "0008_rename_groups_openidloginprevention_teams"),
        ("user_management", "0012_user_company_name"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="company_name",),
        migrations.RemoveField(model_name="user", name="subscription",),
        migrations.AddField(
            model_name="user",
            name="team",
            field=models.ManyToManyField(
                blank=True,
                help_text="The teams this user belongs to. A user will get all permissions granted to each of their teams.",
                related_name="team_set",
                to="privilege_manager.team",
                verbose_name="teams",
            ),
        ),
    ]