# Generated by Django 3.1.5 on 2021-02-08 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0022_auto_20210122_2030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='is_private',
            new_name='is_archived',
        ),
        migrations.AddField(
            model_name='item',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]
