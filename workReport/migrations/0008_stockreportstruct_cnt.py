# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-12 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workReport', '0007_workreport_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockreportstruct',
            name='cnt',
            field=models.FloatField(default=0),
        ),
    ]
