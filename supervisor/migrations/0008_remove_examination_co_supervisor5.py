# Generated by Django 4.1.3 on 2022-11-09 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supervisor', '0007_delete_examattendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examination',
            name='co_supervisor5',
        ),
    ]
