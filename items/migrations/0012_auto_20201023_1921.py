# Generated by Django 3.1.2 on 2020-10-23 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0011_auto_20201022_0244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtag',
            name='items',
        ),
        migrations.AddField(
            model_name='item',
            name='hashtags',
            field=models.ManyToManyField(related_name='item', to='items.HashTag'),
        ),
    ]
