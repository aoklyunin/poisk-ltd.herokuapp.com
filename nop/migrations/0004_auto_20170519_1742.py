# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-19 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nop', '0003_worker_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='workplace',
            name='department',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='workplace',
            name='number',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='workplace',
            name='sector',
            field=models.IntegerField(default=1),
        ),
    ]
