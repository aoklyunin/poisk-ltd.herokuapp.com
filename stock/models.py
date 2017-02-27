# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Extradition(models.Model):
    date = models.DateField(default=datetime.date.today)
    limit = models.Q(app_label='workReport', model='Equipment') \
            | models.Q(app_label='workReport', model='AssemblyUnit') \
            | models.Q(app_label='workReport', model='Detail')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.tag
