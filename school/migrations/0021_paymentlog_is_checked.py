# Generated by Django 4.1.7 on 2023-03-14 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0020_payment_status_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentlog',
            name='is_checked',
            field=models.BooleanField(blank=True, null=True, verbose_name='платеж проверен'),
        ),
    ]
