# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-12 02:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='thumb',
            new_name='thumbnail',
        ),
    ]
