# Generated by Django 3.0.7 on 2020-06-20 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20200613_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='total_likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
