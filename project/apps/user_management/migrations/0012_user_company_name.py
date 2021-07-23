# Generated by Django 3.0 on 2021-07-23 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0011_auto_20210722_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company_name',
            field=models.CharField(blank=True, help_text='Associated company name', max_length=250, null=True),
        ),
    ]
