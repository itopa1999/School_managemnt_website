# Generated by Django 3.2.4 on 2022-10-24 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0006_auto_20221024_0314'),
        ('student', '0004_remove_token_student'),
        ('users', '0005_user_dep'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Faculty',
        ),
    ]