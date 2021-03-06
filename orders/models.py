# -*- coding: utf-8 -*-
from django.db import models

from plan.models import Customer, Agreement


class Order(models.Model):
    # заказчик
    customer = models.ForeignKey(Customer)
    # номер заказа
    number = models.CharField(max_length=500)
    # название заказа
    name = models.CharField(max_length=500)
    # наличие военной прниёмки
    needVP = models.BooleanField(default=False)
    # примечание
    note = models.CharField(max_length=10000)
    # договор
    agreement = models.ForeignKey(Agreement)
    # статус
    status = models.IntegerField(default=0)
    # дата запуска
    startDate = models.DateField('date start')
    # дата по договору
    agreementDate = models.DateField('date agreement')
    # дата по плану
    planDate = models.DateField('date plan')
    # необходимые объекты для данной работы
    needStruct = models.ManyToManyField('constructors.NeedStruct', blank=True, default=None)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
