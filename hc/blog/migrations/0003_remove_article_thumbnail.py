# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-12 02:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180712_0256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='thumbnail',
        ),
    ]
