# Generated by Django 3.1.2 on 2020-10-23 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0012_auto_20201023_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='hashtags',
            field=models.ManyToManyField(related_name='items', to='items.HashTag'),
        ),
    ]
