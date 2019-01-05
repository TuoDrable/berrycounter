# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-01-05 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='counter',
            name='pulses_this_hour',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='counter',
            name='name',
            field=models.CharField(choices=[('RW', 'Regenwater'), ('GAS', 'Gas'), ('DW', 'Stadswater')], max_length=100),
        ),
    ]