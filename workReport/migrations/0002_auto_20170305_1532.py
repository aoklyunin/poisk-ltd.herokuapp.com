# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-05 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workReport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workpart',
            name='scheme',
            field=models.ManyToManyField(blank=True, default=None, to='plan.Scheme'),
        ),
    ]