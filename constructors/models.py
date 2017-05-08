# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from plan.models import WorkerPosition, Scheme, Area


# Что хранится на складе
class StockStruct(models.Model):
    cnt = models.FloatField(default=0)
    area = models.ForeignKey(Area)

    def __str__(self):
        return self.area.name + " (" + str(self.cnt) + ")"


# сколько чего надо по тех. процессу
class NeedStruct(models.Model):
    equipment = models.ForeignKey('Equipment', blank=True, default=None)
    cnt = models.FloatField(default=0)
    completeCnt = models.FloatField(default=0)

    def __str__(self):
        if self.equipment != None:
            return str(self.equipment) + " " + str(self.cnt)
        return ""


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
    # длительность
    duration = models.FloatField(default=0)

    def getSchemeChoices(self):
        lst = []
        for sch in self.scheme.all():
            lst.append(str(sch.pk))
        return lst

    def generateDataFromNeedStructs(self):
        arr = []
        for ns in self.needStruct.all():
            if (ns.equipment != None):
                arr.append({'equipment': str(ns.equipment.pk),
                            'cnt': str(ns.cnt)})
        return arr

    def generateDataFromNeedStructsNET(self, NeedEquipmentType):
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
        s = self.name + "("
        if self.equipmentType == self.TYPE_STANDART_WORK:
            s += " "+str(self.duration)+" "
        return s+self.dimension + ")"

    def __unicode__(self):
        return self.name + "(" + self.dimension + ")"

    def addFromFormset(self, formset, doCrear=False):
        if (doCrear):
            for ns in self.needStruct.all():
                ns.delete()
            self.needStruct.clear()

        if formset.is_valid():
            for form in formset.forms:
                if form.is_valid:
                    d = form.cleaned_data
                    if (len(d) > 0) and  ("cnt" in d) and (float(d["cnt"])>0) and\
                            (("equipment" in d) and (not d["equipment"] is None) and (d["equipment"] != self)):

                        ns = NeedStruct.objects.create(equipment=Equipment.objects.get(pk=int(d["equipment"])),
                                                   cnt=float(d["cnt"]))
                        print(ns)
                        ns.save()
                        self.needStruct.add(ns)
                else:
                    print("for is not valid")

    # константы
    # стандартные работы обязательно должны быть последними
    # типы оборудования
    TYPE_INSTUMENT = 0
    TYPE_MATERIAL = 1
    TYPE_DETAIL = 2
    TYPE_ASSEMBLY_UNIT = 3
    TYPE_STANDART_WORK = 4
    # названия групп
    EQUIPMENT_LABELS = [
        "Инструмент",
        "Комплетующие",
        "Детали",
        "Сборочные единицы",
        "Стандартные работы",
    ]
    EQUIPMENT_TYPE_COUNT = len(EQUIPMENT_LABELS)
    CONSTRUCTOR_ENABLED = [
        2, 3, 4
    ]
    # формируем список для конструкторов
    CONSTRUCTOR_CHOICES = []
    for i in CONSTRUCTOR_ENABLED:
        CONSTRUCTOR_CHOICES.append((str(i), EQUIPMENT_LABELS[i]))
    # формируем общий список
    CHOICES = []
    for i in range(EQUIPMENT_TYPE_COUNT):
        CHOICES.append((str(i), EQUIPMENT_LABELS[i]))


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
