# Generated by Django 4.1.3 on 2022-11-17 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0036_alter_course_semester_alter_exam_timetable_week_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateField(),
        ),
    ]
