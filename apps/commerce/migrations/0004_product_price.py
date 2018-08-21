# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-27 22:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0003_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10.99, max_digits=10),
            preserve_default=False,
        ),
    ]
