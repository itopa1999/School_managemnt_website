# Generated by Django 3.2.4 on 2022-10-27 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_auto_20221027_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam_timetable',
            name='supervisor',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
