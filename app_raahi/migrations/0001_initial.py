# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 20:17
from __future__ import unicode_literals

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
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='users/profile')),
                ('facebook_id', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook_token', models.CharField(blank=True, max_length=255, null=True)),
                ('friends', models.ManyToManyField(blank=True, related_name='friends_list', to='app_raahi.UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
