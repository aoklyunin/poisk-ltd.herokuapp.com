# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-03 08:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_auto_20170302_0953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moveassembly',
            name='assembly',
        ),
        migrations.RemoveField(
            model_name='movedetail',
            name='detail',
        ),
        migrations.DeleteModel(
            name='MoveAssembly',
        ),
        migrations.DeleteModel(
            name='MoveDetail',
        ),
    ]