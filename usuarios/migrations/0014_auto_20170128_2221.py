# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-28 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0013_auto_20170123_0642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anunc',
            name='mensaje',
            field=models.TextField(blank=True, max_length=150),
        ),
    ]
