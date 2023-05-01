# Generated by Django 4.1.7 on 2023-02-16 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_alter_lesson_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='review',
        ),
        migrations.AddField(
            model_name='lesson',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='lessons/', verbose_name='превью'),
        ),
    ]
