# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import django
from django.db import models

# Create your models here.
from constructors.models import NeedStruct, Equipment
#from nop.models import WorkPlace
from nop.models import WorkPlace, Worker
from plan.models import Agreement, Customer

# причина проёба
from stock.models import Provider


class Excuse(models.Model):
    author = models.ForeignKey(Worker)
    text =  models.TextField(max_length=100000, null=True, blank=True)


# Часть проекта при планировании (например, какая-нибудь работа или деталь)
class PlanEquipmentPart(models.Model):
    # оборудование
    equipment = models.ForeignKey(Equipment)
    # планируемое кол-во
    planCnt = models.FloatField(default=1)
    # текущее кол-во
    curCnt = models.FloatField(default=0)
    # изначальная дата
    sDate = models.DateField(default=django.utils.timezone.now)
    # планируемая дата( может меняться)
    pDate = models.DateField(default=django.utils.timezone.now)
    # фактическая дата( выставляется, когда всё выполнено)
    fDate = models.DateField(default=django.utils.timezone.now)
    # выполнена ли эта часть
    complete = models.BooleanField(default=False)
    # причина задержки может быть пустой только если фактическая дата со стартовой
    excuses = models.ManyToManyField(Excuse,null=True, blank=True)
    # кооперация (если пустое поле, то делается в Поиске)
    cooperation = models.ForeignKey(Provider,null=True, blank=True)
    # исполнитель
    worker = models.ForeignKey(Worker)
    # можно ли редактировать
    canEdit = models.BooleanField(default=True)
    # нужна ли приёмка ОТК
    needVIK = models.BooleanField(default=False)
    # рабочее место (обязательно  для стандартных работ, если нет кооперации)
    workPlace = models.ForeignKey(WorkPlace, null=True, blank=True)
    # время начала выполнения
    startTime = models.TimeField(default=django.utils.timezone.now)
    # время конца выполнения
    endTime = models.TimeField(default=django.utils.timezone.now)

    class Meta:
        ordering = ['pDate']


# класс проекта
class Project(models.Model):
    # название
    name = models.TextField(max_length=100000, null=True, blank=True)
    # ответственный
    charge = models.ForeignKey(Worker)
    # части работ
    peParts = models.ManyToManyField(PlanEquipmentPart,null=True, blank=True)

    def __str__(self):
        return self.pageName

