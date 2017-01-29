# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models

from workReport.models import Equipment, Scheme
from workReport.models import Material

from workReport.workReportGenerator import generateReport


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



# класс сборочных единиц
class AssemblyUnits(models.Model):
    # сборочные единицы
    assemblyUnits = models.ManyToManyField("self")
    # оснаска и комплектующие
    equipment = models.ManyToManyField(Equipment)
    # материалы
    materials = models.ManyToManyField(Material)
    # имя
    name = models.CharField(max_length=1000)
    # чертёж
    scheme = models.ManyToManyField(Scheme)
    # шифр
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name




# инструмент
class Instrument(models.Model):
    # название
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name




class Orders(models.Model):
    # сборочные единицы
    assemblyUnits = models.ManyToManyField(AssemblyUnits)
    # оснаска и комплектующие
    equipment = models.ManyToManyField(Equipment)
    # материалы
    materials = models.ManyToManyField(Material)
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

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
