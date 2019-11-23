# Generated by Django 2.2.7 on 2019-11-22 03:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ImageField(blank=True, null=True, upload_to='')),
                ('caption', models.TextField(blank=True, max_length=150, null=True)),
                ('likes_count', models.PositiveIntegerField(default=0)),
                ('comments_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_like', to='items.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('item', 'user')},
            },
        ),
    ]