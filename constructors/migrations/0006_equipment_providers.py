# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-09 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_provider'),
        ('constructors', '0005_auto_20170509_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='providers',
            field=models.ManyToManyField(to='stock.Provider'),
        ),
    ]
