# Generated by Django 3.2.4 on 2022-10-29 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0009_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
