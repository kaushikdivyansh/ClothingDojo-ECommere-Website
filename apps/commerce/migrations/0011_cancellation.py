# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-29 01:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0010_order_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cancellation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_created_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cancellation_users', to='commerce.User')),
            ],
        ),
    ]
