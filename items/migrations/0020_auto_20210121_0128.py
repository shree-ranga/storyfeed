# Generated by Django 3.1.2 on 2021-01-21 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0019_auto_20210121_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status_blue',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='status_green',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='status_red',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]