# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#from nop.models import WorkPlace
from nop.models import WorkPlace, Worker, Area
from stock.models import Provider

class Scheme(models.Model):
    # автор
    author = models.ForeignKey(Worker)
    # шифр
    code = models.CharField(max_length=1000)
    # ссылка
    link = models.CharField(max_length=100)

    def __unicode__(self):
        return self.code+" : "+str(self.author)

    def __str__(self):
        return self.code + " : " + str(self.author)


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
    scheme = models.ManyToManyField(Scheme, blank=True, null=True)
    # склад
    stockStruct = models.ManyToManyField(StockStruct, blank=True, default=None)
    # нужно ли ОТК
    needVIK = models.BooleanField(default=False)
    # необходимые объекты для данной работы
    needStruct = models.ManyToManyField(NeedStruct, blank=True, default=None,
                                        related_name="needStructStandartWork12")
    # длительность
    duration = models.FloatField(default=0, null=True, blank=True)
    # поставщикик
    providers = models.ManyToManyField(Provider, blank=True, null=True, default=None,)
    # оборудование, получаемое в ходе работ
    genEquipment = models.ManyToManyField(NeedStruct, blank=True, default=None,
                                        related_name="genEquipment12")
    workPlaces = models.ManyToManyField(WorkPlace, blank=True, default=None)

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

    def generateDataFromGenEquipment(self):
        arr = []
        for ns in self.genEquipment.all():
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


    def saveProvidersAndShemes(self, form):
        if form.is_valid():

            self.scheme.clear()
            for scheme in form.cleaned_data["scheme"]:
                self.scheme.add(scheme)

            self.providers.clear()
            for provider in form.cleaned_data["providers"]:
                self.providers.add(provider)

            self.save()

    def addGenEquipmentFromFormset(self, formset, doCrear=False):
        if (doCrear):
            for ns in self.genEquipment.all():
                ns.delete()
            self.genEquipment.clear()

        if formset.is_valid():
            for form in formset.forms:
                if form.is_valid:
                    try:
                        d = form.cleaned_data
                        ns = NeedStruct.objects.create(equipment=Equipment.objects.get(pk=int(d["equipment"])),
                                                       cnt=float(d["cnt"]))
                        ns.save()
                        self.genEquipment.add(ns)
                    except:
                        print("ошибка работы формы из формсета gen-equipment")
                else:
                    print("for is not valid")

    def addFromFormset(self, formset, doCrear=False):
        if (doCrear):
            for ns in self.needStruct.all():
                ns.delete()
            self.needStruct.clear()

        if formset.is_valid():
            for form in formset.forms:
                if form.is_valid:
                    try:
                        d = form.cleaned_data
                        ns = NeedStruct.objects.create(equipment=Equipment.objects.get(pk=int(d["equipment"])),
                                                        cnt=float(d["cnt"]))
                        ns.save()
                        self.needStruct.add(ns)
                    except:
                        print("ошибка работы формы из формсета need-equipment")
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
    STOCK_ENABLED = [
        0, 1
    ]
    # формируем список для конструкторов
    CONSTRUCTOR_CHOICES = []
    for i in CONSTRUCTOR_ENABLED:
        CONSTRUCTOR_CHOICES.append((str(i), EQUIPMENT_LABELS[i]))
    # формируем общий список
    CHOICES = []
    for i in range(EQUIPMENT_TYPE_COUNT):
        CHOICES.append((str(i), EQUIPMENT_LABELS[i]))
    # формируем список для склада
    STOCK_CHOICES = []
    for i in STOCK_ENABLED:
        STOCK_CHOICES.append((str(i), EQUIPMENT_LABELS[i]))
    class Meta:
        ordering = ['name']