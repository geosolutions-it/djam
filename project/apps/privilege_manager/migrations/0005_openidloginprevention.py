# Generated by Django 3.0 on 2020-02-06 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oidc_provider', '0026_client_multiple_response_types'),
        ('privilege_manager', '0004_auto_20200127_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenIdLoginPrevention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groups', models.ManyToManyField(blank=True, to='privilege_manager.Group')),
                ('oidc_client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='oidc_provider.Client')),
            ],
            options={
                'verbose_name': 'OpenID Login Prevention',
                'verbose_name_plural': 'OpenID Login Preventions',
            },
        ),
    ]
