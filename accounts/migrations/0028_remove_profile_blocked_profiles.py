# Generated by Django 3.0.7 on 2020-07-09 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20200709_2248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='blocked_profiles',
        ),
    ]