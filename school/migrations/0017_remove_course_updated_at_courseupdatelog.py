# Generated by Django 4.1.7 on 2023-03-13 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0016_lesson_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='updated_at',
        ),
        migrations.CreateModel(
            name='CourseUpdateLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.DateTimeField(auto_now=True, verbose_name='последнее изменение')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.course')),
            ],
        ),
    ]