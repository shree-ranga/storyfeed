# Generated by Django 3.1.2 on 2020-10-22 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0010_item_audio_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='engagement_counter',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='item',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('items', models.ManyToManyField(related_name='hashtags', to='items.Item')),
            ],
        ),
    ]
