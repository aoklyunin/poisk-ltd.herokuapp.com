# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from plan.models import WorkerPosition, Scheme, Area


# Что хранится на складе
class StockStruct(models.Model):
    cnt = models.FloatField(default=0)
    area = models.ForeignKey(Area)


# сколько чего надо по тех. процессу
class NeedStruct(models.Model):
    equipment = models.ForeignKey('Equipment', blank=True, default=None)
    cnt = models.FloatField(default=0)
    completeCnt = models.FloatField(default=0)

    def __str__(self):
        if self.equipment != None:
            return str(self.equipment) + " " + str(self.cnt)
        else:
            return str(self.standartWork) + " " + str(self.cnt)


class Equipment(models.Model):
    # название
    name = models.CharField(max_length=1000, default="")
    # единица измерения
    dimension = models.CharField(max_length=200, default="")
    # шифр
    code = models.CharField(max_length=100, blank=True, default="", null=True)
    # тип
    equipmentType = models.IntegerField(default=0)
    # чертёж
    scheme = models.ManyToManyField(Scheme, blank=True)
    # склад
    stockStruct = models.ManyToManyField(StockStruct, blank=True, default=None)
    # нужно ли ОТК
    needVIK = models.BooleanField(default=False)
    # необходимые объекты для данной работы
    needStruct = models.ManyToManyField(NeedStruct, blank=True, default=None,
                                        related_name="needStructStandartWork12")
    TYPE_INSTUMENT = 0
    TYPE_MATERIAL = 1
    TYPE_DETAIL = 2
    TYPE_ASSEMBLY_UNIT = 3
    TYPE_STANDART_WORK = 4

    EQUIPMENT_LABELS = [
        "Инструмент",
        "Комплетующие",
        "Детали",
        "Сборочные единицы",
        "Стандартные работы",
    ]

    EQUIPMENT_TYPE_COUNT = 5

    duration = models.FloatField(default=0)

    def generateDataFromNeedStructs(self, NeedEquipmentType):
        arr = []
        for ns in self.needStruct.all():
            if (ns.equipment != None) and (ns.equipment.equipmentType == NeedEquipmentType):
                arr.append({'equipment': ns.equipment,
                            'cnt': ns.cnt})
            elif (ns.standartWork != None):
                arr.append({'standartWork': ns.standartWork,
                            'cnt': ns.cnt})
        return arr

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def addFromFormset(self, formset, doCrear=False):
        if (doCrear):
            for ns in self.needStruct.all():
                ns.delete()
            self.needStruct.clear()

        if formset.is_valid():
            for form in formset.forms:
                d = form.cleaned_data
                if (len(d) > 0) and \
                        (("equipment" in d) and (not d["equipment"] is None) and (d["equipment"] != self) or (
                                    ("standartWork" in d) and (not d["standartWork"] is None))):
                    print(d)
                    ns = NeedStruct.objects.create(**d)
                    ns.save()
                    self.needStruct.add(ns)


class MyEquipment(models.Model):
    equipment = models.ManyToManyField("constructors.Equipment")

    def __str__(self):
        return str(self.equipment) + ":" + str(self.cnt)

    def accept(self, area_id):
        if int(area_id) == 0:
            area = Area.objects.get(name="Красное село")
        else:
            area = Area.objects.get(name="Малахит")

        ss = self.equipment.stockStruct.get(area=area)
        if self.flgAcceptance:
            ss.cnt += self.cnt
        else:
            ss.cnt -= self.cnt
        ss.save()


