# Generated by Django 3.0.7 on 2020-06-09 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_profile_all_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, height_field=300, null=True, upload_to='', width_field=300),
        ),
    ]
