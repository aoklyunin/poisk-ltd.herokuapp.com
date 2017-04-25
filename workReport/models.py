# -*- coding: utf-8 -*-
import datetime

from django.db import models

from constructors.models import StandartWork, NeedStruct, Equipment
from orders.models import Order
from plan.models import Agreement, Scheme, WorkerPosition, WorkPlace, Rationale, Worker, Area
from plan.models import Customer
from workReport.workReportGenerator import generateReport


# сколько по складу
class StockReportStruct(models.Model):
    # оборудование
    equipment = models.ForeignKey('constructors.Equipment', blank=True)
    # выдано
    getCnt = models.FloatField(default=0)
    # брак
    rejectCnt = models.FloatField(default=0)
    # утиль
    dustCnt = models.FloatField(default=0)
    # возвращено
    returnCnt = models.FloatField(default=0)



# Часть наряда
class WorkPart(models.Model):
    comment = models.CharField(max_length=2000, blank=True, default="", null=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    standartWork = models.ForeignKey(Equipment)
    workPlace = models.ForeignKey(WorkPlace, blank=True, default=None, null=True)
    rationale = models.ForeignKey(Rationale, blank=True, default=None, null=True)
    scheme = models.ManyToManyField(Scheme, blank=True, default=None)

    def __str__(self):
        return self.startTime.strftime("%H:%M") + "-" + self.endTime.strftime("%H:%M") + " " \
               + str(self.standartWork) + " " + self.comment

    def __unicode__(self):
        return self.startTime.strftime("%H:%M") + "-" + self.endTime.strftime("%H:%M") + " " + str(
            self.standartWork) + " " + self.comment


# брак
class Reject(models.Model):
    # деталь
    needs = models.ManyToManyField(NeedStruct, blank=True)

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
                                          blank=True)
    # внеплановая выдача комплектующих
    noPlanHardware = models.ManyToManyField(StockReportStruct, verbose_name='Внеплановая',
                                            related_name="no_PlanHardware_name", blank=True)
    # брак
    rejected = models.ManyToManyField(Reject, blank=True)
    # выполняемые работы
    workPart = models.ManyToManyField(WorkPart, related_name="work_Part", blank=True)
    # фактически выполненные работы
    factWorkPart = models.ManyToManyField(WorkPart, related_name="fact_WorkPart", blank=True)
    # примечание
    note = models.CharField(max_length=10000, default="", blank=True, null=True)
    # флаг для первого обсчёта плановой выдачи оборудования
    flgCalculateEquipment = models.BooleanField(default=False)
    # заказ по которому выполняется наряд
    order = models.ForeignKey(Order, blank=True, null=True)
    # флаг, что подобраны исполнители
    flgCalculateWorkers = models.BooleanField(default=False)
    # нужен ли вик
    needVIK = models.BooleanField(default=False)
    # площадка
    area = models.IntegerField(default=0)

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
