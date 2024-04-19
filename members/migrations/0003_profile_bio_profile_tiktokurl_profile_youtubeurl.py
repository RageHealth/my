# Generated by Django 5.0.2 on 2024-04-15 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tiktokurl',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='youtubeurl',
            field=models.URLField(blank=True),
        ),
    ]