# Generated by Django 4.1.7 on 2023-03-12 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0013_alter_lesson_slug_alter_payment_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='date',
        ),
        migrations.AddField(
            model_name='payment',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата оплаты'),
        ),
    ]