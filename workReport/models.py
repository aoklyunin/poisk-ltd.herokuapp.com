# -*- coding: utf-8 -*-
import datetime

from django.db import models

from plan.models import Agreement, Scheme, WorkerPosition, WorkPlace, Rationale, Worker, Area
from plan.models import Customer
from workReport.workReportGenerator import generateReport


# Что хранится на складе
class StockStruct(models.Model):
    cnt = models.FloatField(default=0)
    area = models.ForeignKey(Area)


# сколько по складу
class StockReportStruct(models.Model):
    # оборудование
    equipment = models.ForeignKey('Equipment', blank=True)
    # детали
    detail = models.ForeignKey('Detail', blank=True)
    # сборочные единицы
    assemblyUnit = models.ForeignKey('AssemblyUnit', blank=True)
    # выдано
    getCnt = models.FloatField(default=0)
    # брак
    rejectCnt = models.FloatField(default=0)
    # утиль
    dustCnt = models.FloatField(default=0)
    # возвращено
    returnCnt = models.FloatField(default=0)


class Equipment(models.Model):
    # название
    name = models.CharField(max_length=1000, default="Перчатки")
    # единица измерения
    dimension = models.CharField(max_length=200, default="Пара")
    # шифр
    code = models.CharField(max_length=100, blank=True, default="", null=True)
    # тип
    equipmentType = models.IntegerField(default=0)
    # чертёж
    scheme = models.ManyToManyField(Scheme, blank=True, null=True)
    # склад
    stockStruct = models.ManyToManyField(StockStruct, blank=True, null=True)
    # нужно ли ОТК
    needVIK = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# сколько чего надо по тех. процессу
class NeedStruct(models.Model):
    equipment = models.ForeignKey('Equipment', blank=True)
    standartWork = models.ForeignKey('StandartWork', blank=True)
    detail = models.ForeignKey('Detail', blank=True)
    assemblyUnit = models.ForeignKey('AssemblyUnit', blank=True)
    cnt = models.FloatField(default=0)


# стандартная работа
class StandartWork(models.Model):
    # название
    text = models.CharField(max_length=2000)
    # должности, которые могут выполнять
    positionsEnable = models.ManyToManyField(WorkerPosition)
    # необходимые объекты для данной работы
    needStruct = models.ManyToManyField(NeedStruct, blank=True, default=None, null=True,
                                        related_name="needStructStandartWork")
    #  длительность в минутах
    duration = models.FloatField(default=0)
    # нужно ли ОТК
    needVIK = models.BooleanField(default=False)

    def __str__(self):
        return self.text + "(" + str(self.duration) + ")"

    def __unicode__(self):
        return self.text + "(" + str(self.duration) + ")"


# Часть наряда
class WorkPart(models.Model):
    comment = models.CharField(max_length=2000, blank=True, default="", null=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    standartWork = models.ForeignKey(StandartWork)
    workPlace = models.ForeignKey(WorkPlace, blank=True, default=None, null=True)
    rationale = models.ForeignKey(Rationale, blank=True, default=None, null=True)
    scheme = models.ManyToManyField(Scheme, blank=True, default=None, null=True)

    def __str__(self):
        return self.startTime.strftime("%H:%M") + "-" + self.endTime.strftime("%H:%M") + " " \
               + str(self.standartWork) + " " + self.comment

    def __unicode__(self):
        return self.startTime.strftime("%H:%M") + "-" + self.endTime.strftime("%H:%M") + " " + str(
            self.standartWork) + " " + self.comment


class Detail(models.Model):
    # шифр
    code = models.CharField(max_length=100)
    # имя
    name = models.CharField(max_length=1000)
    # чертёж
    scheme = models.ManyToManyField(Scheme, blank=True, default=None, null=True)
    # необходимые объекты для данной работы
    needStruct = models.ManyToManyField(NeedStruct, blank=True, default=None, null=True,
                                        related_name="needStructDetail123")
    # склад
    stockStruct = models.ManyToManyField(StockStruct)
    # нужно ли ОТК
    needVIK = models.BooleanField(default=False)


# класс сборочных единиц
class AssemblyUnit(models.Model):
    # имя
    name = models.CharField(max_length=1000)
    # чертёж
    scheme = models.ManyToManyField(Scheme, blank=True, default=None, null=True)
    # шифр
    code = models.CharField(max_length=100, default="")
    # необходимые объекты для данной работы
    needStruct = models.ManyToManyField(NeedStruct, blank=True, default=None, null=True,
                                        related_name="needStructAssemblyUnit")
    # склад
    stockStruct = models.ManyToManyField(StockStruct)
    # нужно ли ОТК
    needVIK = models.BooleanField(default=False)


    # сдандартные работы
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


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
    needStruct = models.ManyToManyField(NeedStruct, blank=True, default=None, null=True)

    # описание тех.процеса
    # tehReview = models.ForeignKey(TehReview)
    # нужно ли
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# брак
class Reject(models.Model):
    # деталь
    needs = models.ManyToManyField(NeedStruct, blank=True, null=True)

    def __unicode__(self):
        if self.equipment != None:
            return self.equipment.name
        else:
            return self.material.name

    def __str__(self):
        if self.equipment != None:
            return self.equipment.name
        else:
            return self.material.name


# наряд
class WorkReport(models.Model):
    # руководитель
    supervisor = models.ForeignKey(Worker, verbose_name='Руководитель', related_name="supervisor_name", blank=True,
                                   null=True)
    # ответственный за ВИК
    VIKer = models.ForeignKey(Worker, verbose_name='ВИК', related_name="VIKER_name", blank=True, null=True)
    # исполнитель
    worker = models.ForeignKey(Worker, verbose_name='Иcполнитель', related_name="worker_name", blank=True, null=True)
    # кладовщик
    stockMan = models.ForeignKey(Worker, verbose_name='Кладовщик', related_name="stockMan_name", blank=True, null=True)
    # составитель отчёта
    reportMaker = models.ForeignKey(Worker, verbose_name='Cоставитель отчёта', related_name="reportMaker_name",
                                    blank=True, null=True)
    # проверяющий отчёт
    reportChecker = models.ForeignKey(Worker, verbose_name='Проверяющий отчёт', related_name="reportChecker_name",
                                      blank=True, null=True)
    # дата
    adate = models.DateField(default=datetime.date.today)
    # дата ВИК
    VIKDate = models.DateField(default=datetime.date.today)
    # плановая выдача комплектующих
    planHardware = models.ManyToManyField(StockReportStruct, verbose_name='Плановая', related_name="planHardware_name",
                                          blank=True, null=True)
    # внеплановая выдача комплектующих
    noPlanHardware = models.ManyToManyField(StockReportStruct, verbose_name='Внеплановая',
                                            related_name="no_PlanHardware_name", blank=True, null=True)
    # брак
    rejected = models.ManyToManyField(Reject, blank=True, null=True)
    # выполняемые работы
    workPart = models.ManyToManyField(WorkPart, related_name="work_Part", blank=True, null=True)
    # фактически выполненные работы
    factWorkPart = models.ManyToManyField(WorkPart, related_name="fact_WorkPart", blank=True, null=True)
    # примечание
    note = models.CharField(max_length=10000, default="", blank=True, null=True)
    # флаг для первого обсчёта плановой выдачи оборудования
    flgCalculateEquipment = models.BooleanField(default=False)
    # заказ по которому выполняется наряд
    order = models.ForeignKey(Order, blank=True)
    # флаг, что подобраны исполнители
    flgCalculateWorkers = models.BooleanField(default=False)
    # нужен ли вик
    needVIK = models.BooleanField(default=False)

    def generateDoc(self):
        wp = []
        i = 0
        for wPart in self.workPart.all().order_by('startTime'):
            i += 1
            if wPart.workPlace is None:
                wpname = "-"
            else:
                wpname = wPart.workPlace.name
            wp.append(
                [str(i), wpname, wPart.standartWork.text + " " + wPart.comment, wPart.startTime.strftime("%H:%M"),
                 wPart.endTime.strftime("%H:%M")])

        fwp = []
        i = 0
        for wPart in self.factWorkPart.all().order_by('startTime'):
            i += 1
            if wPart.workPlace is None:
                wpname = "-"
            else:
                wpname = wPart.workPlace.name
            fwp.append(
                [str(i), wpname, wPart.standartWork.text + " " + wPart.comment, wPart.startTime.strftime("%H:%M"),
                 wPart.endTime.strftime("%H:%M")])

        note = "Примечание 1 (обязательное):\nМаксимальный срок проведения ВИК (входного контроля) до " \
               "конца рабочего дня " + str(self.VIKDate)
        if self.note != "":
            note += "\nПримечание 2:\n" + self.note

        planEquipment = []
        for equip in self.planHardware.all():
            e = []
            if equip.equipment is None:
                e = [equip.material.name, equip.material.code, equip.material.dimension]
            else:
                e = [equip.equipment.name, equip.equipment.code, equip.equipment.dimension]
            for l in [str(equip.getCnt), str(equip.usedCnt), str(equip.rejectCnt), str(equip.dustCnt),
                      str(equip.remainCnt)]:
                e.append(l)
            planEquipment.append(e)

        nonPlanEquipment = []
        for equip in self.noPlanHardware.all():
            e = []
            if equip.equipment is None:
                e = [equip.material.name, equip.material.code, equip.material.dimension]
            else:
                e = [equip.equipment.name, equip.equipment.code, equip.equipment.dimension]
            for l in [str(equip.getCnt), str(equip.usedCnt), str(equip.rejectCnt), str(equip.dustCnt),
                      str(equip.remainCnt)]:
                e.append(l)
            # print(e)
            nonPlanEquipment.append(e)
        dust = []
        for equip in self.rejected.all():
            if equip.equipment is None:
                e = [equip.material.name]
            else:
                e = [equip.equipment.name]
            for l in [str(equip.cnt)]:
                e.append(l)

            dust.append(e)

        attestation = "Аттестация отсутствует"
        if self.worker.attestation.name is not None:
            attestation = self.worker.attestation.name

            # print(attestation)
        # print(wp)
        return generateReport(self.supervisor.getInitials(), self.supervisor.getShort(),
                              self.worker.getShort(), str(self.worker.tnumber), self.stockMan.getShort(),
                              self.adate, self.worker.position.first().name,
                              self.getRationales(), wp, fwp, self.reportMaker.getShort(),
                              self.reportChecker.getShort(), self.VIKer.getShort(), note,
                              attestation, dust, planEquipment, nonPlanEquipment)

    def getRationales(self):
        i = 0
        d = {}
        for part in self.workPart.order_by('startTime'):
            i += 1
            if part.rationale != None:
                if d.get(part.rationale.name):
                    d[part.rationale.name].append(i)
                else:
                    d[part.rationale.name] = [i]
        rationales = []
        for key, value in d.items():
            rationales.append([str(value), key])
        return rationales

    def __str__(self):
        # return "sad"
        if (self.supervisor is None):
            s = ""
        else:
            s = self.supervisor.getInitials()
        s += "-"
        if (self.worker is None):
            s += ""
        else:
            s += str(self.worker.tnumber)
        s += "-"
        if (self.adate is None):
            s += ""
        else:
            s += str(self.adate)
        return s

    def __unicode__(self):
        # return "sad"
        if (self.supervisor is None):
            s = ""
        else:
            s = self.supervisor.getInitials()
        s += "-"
        if (self.worker is None):
            s += ""
        else:
            s += str(self.worker.tnumber)
        s += "-"
        if (self.adate is None):
            s += ""
        else:
            s += str(self.adate)
        return s
