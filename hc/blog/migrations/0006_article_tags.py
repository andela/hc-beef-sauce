# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-12 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180712_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
