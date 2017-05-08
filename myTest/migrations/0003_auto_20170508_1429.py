# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-08 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myTest', '0002_author_bookchoose'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.RemoveField(
            model_name='bookchoose',
            name='book',
        ),
        migrations.AddField(
            model_name='bookchoose',
            name='book',
            field=models.ManyToManyField(to='myTest.Book'),
        ),
    ]