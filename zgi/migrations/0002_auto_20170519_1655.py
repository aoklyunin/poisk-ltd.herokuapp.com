# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-19 13:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zgi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planequipmentpart',
            name='fDate',
            field=models.DateField(default=datetime.datetime(2017, 5, 19, 16, 55, 53, 392471)),
        ),
        migrations.AlterField(
            model_name='planequipmentpart',
            name='pDate',
            field=models.DateField(default=datetime.datetime(2017, 5, 19, 16, 55, 53, 392471)),
        ),
        migrations.AlterField(
            model_name='planequipmentpart',
            name='sDate',
            field=models.DateField(default=datetime.datetime(2017, 5, 19, 16, 55, 53, 392471)),
        ),
    ]
