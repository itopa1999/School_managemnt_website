# Generated by Django 4.1.3 on 2022-11-21 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0045_remove_register_course_course1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='register_course',
            name='course_unit',
            field=models.PositiveIntegerField(default=False),
        ),
    ]
