# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-02 16:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workReport', '0003_auto_20170302_0758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='equipment',
        ),
    ]