# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-04 21:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=300)),
                ('status', models.CharField(default='pending', max_length=40)),
                ('time', models.TimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='dob',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='first_app.User'),
        ),
    ]
