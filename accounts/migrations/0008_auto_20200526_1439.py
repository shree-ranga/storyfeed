# Generated by Django 3.0.5 on 2020-05-26 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200526_0346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='report_count',
        ),
        migrations.AddField(
            model_name='user',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='report_count',
            field=models.IntegerField(default=0),
        ),
    ]
