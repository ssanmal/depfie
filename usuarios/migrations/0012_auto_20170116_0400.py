# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 04:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0011_auto_20170115_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anunc',
            name='autorizador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_aut', to='usuarios.Userio'),
        ),
    ]
