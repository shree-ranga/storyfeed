# Generated by Django 3.0.7 on 2020-07-09 22:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20200709_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='blocked_profiles',
            field=models.ManyToManyField(related_name='blocked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]