# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-19 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
        ('constructors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='providers',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='stock.Provider'),
        ),
    ]