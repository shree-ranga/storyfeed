# Generated by Django 3.0.5 on 2020-04-04 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='caption',
        ),
        migrations.AddField(
            model_name='item',
            name='item_url',
            field=models.URLField(blank=True, max_length=2000),
        ),
    ]
