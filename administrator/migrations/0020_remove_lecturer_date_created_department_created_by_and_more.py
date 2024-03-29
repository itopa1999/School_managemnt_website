# Generated by Django 4.1.3 on 2022-11-11 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0019_lecturer_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecturer',
            name='date_created',
        ),
        migrations.AddField(
            model_name='department',
            name='created_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='faculty',
            name='created_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='faculty',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='created_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='created_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
