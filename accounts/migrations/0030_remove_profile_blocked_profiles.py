# Generated by Django 3.0.7 on 2020-07-09 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_profile_blocked_profiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='blocked_profiles',
        ),
    ]
