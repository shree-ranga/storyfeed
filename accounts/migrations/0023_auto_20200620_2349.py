# Generated by Django 3.0.7 on 2020-06-20 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20200620_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='total_likes',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]