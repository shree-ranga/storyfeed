# Generated by Django 3.1.5 on 2021-02-12 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0023_auto_20210208_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
