# Generated by Django 3.0.5 on 2020-04-10 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_follow_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
