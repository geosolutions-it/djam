# Generated by Django 3.0 on 2021-08-25 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('privilege_manager', '0005_openidloginprevention'),
        ('administration', '0007_auto_20210825_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysubscription',
            name='groups',
            field=models.ForeignKey(blank=True, limit_choices_to={'name__in': ['enterprise']}, on_delete=django.db.models.deletion.CASCADE, related_name='company_sub_groups', to='privilege_manager.Group'),
        ),
        migrations.AlterField(
            model_name='individualsubscription',
            name='groups',
            field=models.ForeignKey(blank=True, limit_choices_to={'name__in': ['free', 'pro']}, on_delete=django.db.models.deletion.CASCADE, related_name='individual_sub_groups', to='privilege_manager.Group'),
        ),
    ]
