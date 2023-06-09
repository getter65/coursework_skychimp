# Generated by Django 4.1.7 on 2023-03-13 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0017_remove_course_updated_at_courseupdatelog'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonUpdateLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.DateTimeField(auto_now=True, verbose_name='последнее изменение')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.lesson')),
            ],
        ),
    ]
