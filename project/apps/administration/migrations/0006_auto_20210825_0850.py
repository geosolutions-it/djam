# Generated by Django 3.0 on 2021-08-25 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0005_companysubscription_individualsubscription'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='individualsubscription',
            constraint=models.UniqueConstraint(fields=('subscription_ptr_id', 'user'), name='unique_user_per_subscription'),
        ),
    ]
