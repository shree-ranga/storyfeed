# Generated by Django 3.0.7 on 2020-07-09 20:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20200629_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='blocked_profiles',
            field=models.ManyToManyField(related_name='blocked', to=settings.AUTH_USER_MODEL),
        ),
    ]
