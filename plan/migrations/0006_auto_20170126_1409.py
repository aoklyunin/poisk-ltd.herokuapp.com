# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-26 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0005_auto_20170126_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='attestation',
            field=models.ManyToManyField(blank=True, to='plan.Attestation'),
        ),
    ]
