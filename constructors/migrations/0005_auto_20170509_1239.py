# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-09 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('constructors', '0004_auto_20170508_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myequipment',
            name='equipment',
        ),
        migrations.DeleteModel(
            name='MyEquipment',
        ),
    ]