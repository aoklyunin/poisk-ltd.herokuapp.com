# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-02 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workReport', '0002_stockstruct_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='dimension',
            field=models.CharField(default=b'\xd0\x9f\xd0\xb0\xd1\x80\xd0\xb0', max_length=200),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(default=b'\xd0\x9f\xd0\xb5\xd1\x80\xd1\x87\xd0\xb0\xd1\x82\xd0\xba\xd0\xb8', max_length=1000),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='stockStruct',
            field=models.ManyToManyField(blank=True, null=True, to='workReport.StockStruct'),
        ),
    ]
