# Generated by Django 3.0.8 on 2020-07-31 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20200731_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-created_at',)},
        ),
    ]
