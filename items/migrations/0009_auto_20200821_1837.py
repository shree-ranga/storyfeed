# Generated by Django 3.1 on 2020-08-21 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_delete_dummy'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='caption',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='video_url',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
