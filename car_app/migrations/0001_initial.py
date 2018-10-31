# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-25 16:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TruckModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=20, unique=True)),
                ('max_capacity', models.IntegerField(default=0)),
                ('model_description', models.TextField(blank=True, help_text='Enter a brief description of the Truck Model', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TruckNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bort_number', models.CharField(max_length=20, unique=True)),
                ('truck_number_description', models.TextField(blank=True, help_text='Enter a brief description of the Truck Number', max_length=1000, null=True)),
                ('current_weight', models.IntegerField(default=0)),
                ('registration_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('current_work_start_date', models.DateTimeField(blank=True, null=True)),
                ('model_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_app.TruckModel')),
            ],
        ),
    ]
