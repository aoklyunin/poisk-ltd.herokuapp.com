# -*- coding: utf-8 -*-
import datetime

from django.db import models




# договор
class Agreement(models.Model):
    # ссылка на договор
    link = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# заказчик
class Customer(models.Model):  # название организации
    name = models.CharField(max_length=500)
    # телефон
    tel = models.CharField(max_length=15)
    # почта
    mail = models.CharField(max_length=100)
    # контактное лицо
    contactPerson = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


