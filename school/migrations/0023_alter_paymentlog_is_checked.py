# Generated by Django 4.1.7 on 2023-03-14 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0022_alter_paymentlog_is_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentlog',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='платеж проверен'),
        ),
    ]
