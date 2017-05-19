# -*- coding: utf-8 -*-
import datetime


from django.db import models


# договор
#from nop.models import WorkerPosition, Attestation
from nop.models import WorkerPosition, Attestation


class Agreement(models.Model):
    # ссылка на договор
    link = models.CharField(max_length=1000)

    def __str__(self):
        return self.link

    def __unicode__(self):
        return self.link


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
        return self.name + "(" + self.contactPerson + ")"

    def __unicode__(self):
        return self.name + "(" + self.contactPerson + ")"



# обоснование для работы
class Rationale(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name



class InfoText(models.Model):
    text = models.TextField(max_length=100000, null=True, blank=True)
    subText = models.TextField(max_length=100000, null=True, blank=True)
    appendText = models.TextField(max_length=100000, null=True, blank=True)
    caption = models.TextField(max_length=100000, null=True, blank=True)
    pageName = models.TextField(max_length=100000, null=True, blank=True)

    def __str__(self):
        return self.pageName


