# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-26 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_worker_patronymic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='worker',
            old_name='number',
            new_name='tnumber',
        ),
    ]
