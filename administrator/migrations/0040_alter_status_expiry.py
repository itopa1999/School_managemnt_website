# Generated by Django 4.1.3 on 2022-11-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0039_message_profile_pic_notice_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
