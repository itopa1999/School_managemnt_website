# Generated by Django 4.1.3 on 2022-11-13 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0029_alter_status_bg'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='attaccess',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
