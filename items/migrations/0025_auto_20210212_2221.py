# Generated by Django 3.1.5 on 2021-02-12 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0024_auto_20210212_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='expiry_time',
            field=models.PositiveIntegerField(default=7, null=True),
        ),
    ]
