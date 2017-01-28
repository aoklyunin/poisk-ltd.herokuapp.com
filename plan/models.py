# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import strftime
from django.utils.translation import ugettext_lazy as _

# чертёж
from plan.workReportGenerator import generateReport


class Scheme(models.Model):
    # автор
    author = models.CharField(max_length=200)
    # ссылка
    link = models.CharField(max_length=100)

    def __unicode__(self):
        return self.author

    def __str__(self):
        return self.author


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


class Material(models.Model):
    # название
    name = models.CharField(max_length=1000)
    # единица измерения
    dimension = models.CharField(max_length=200)
    # шифр
    code = models.CharField(max_length=100, blank=True, default="", null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# класс детали
class Equipment(models.Model):
    # название
    name = models.CharField(max_length=1000)
    # материалы
    materials = models.ManyToManyField(Material, blank=True, null=True)
    # чертёж
    scheme = models.ManyToManyField(Scheme, blank=True, null=True)
    # шифр
    code = models.CharField(max_length=100, blank=True, default="", null=True)
    # тип
    hardwareType = models.IntegerField(default=0)
    # единица измерения
    dimension = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

        # класс материалов


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


class WorkerPosition(models.Model):
    # название
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# рабочее место
class WorkPlace(models.Model):
    # название
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


# аттестация
class Attestation(models.Model):
    # название
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# работник
class Worker(models.Model):
    # должность
    position = models.ManyToManyField(WorkerPosition)
    # аттестация
    attestation = models.ManyToManyField(Attestation, blank=True)
    # привилегии
    privilege = models.IntegerField(default=0)
    # пользователь
    user = models.OneToOneField(User)
    # табельный номер
    tnumber = models.IntegerField()
    # отчество
    patronymic = models.CharField(max_length=200)

    def getInitials(self):
        return self.user.last_name[0] + self.user.first_name[0] + self.patronymic[0]

    def getShort(self):
        return self.user.last_name + " " + self.user.first_name[0] + ". " + self.patronymic[0] + "."

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name


# инструмент
class Instrument(models.Model):
    # название
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


# оснаска и комплектующие
class HardwareEquipment(models.Model):
    # деталь
    equipment = models.ForeignKey(Equipment, blank=True, null=True)
    # материал
    material = models.ForeignKey(Material, blank=True, null=True)
    usedCnt = models.FloatField(default=0)
    getCnt = models.FloatField(default=0)
    rejectCnt = models.FloatField(default=0)
    dustCnt = models.FloatField(default=0)
    remainCnt = models.FloatField(default=0)

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


# брак
class Reject(models.Model):
    # деталь
    equipment = models.ForeignKey(Equipment, blank=True, null=True)
    # материал
    material = models.ForeignKey(Material, blank=True, null=True)
    # кол-во
    cnt = models.FloatField(default=0)

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


# обоснование для работы
class Rationale(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# стандартная работа
class StandartWork(models.Model):
    text = models.CharField(max_length=2000)
    positionsEnable = models.ManyToManyField(WorkerPosition)

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text


# Часть наряда
class WorkPart(models.Model):
    comment = models.CharField(max_length=2000, blank=True, default="", null=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    standartWork = models.ForeignKey(StandartWork)
    workPlace = models.ForeignKey(WorkPlace, blank=True, default=None, null=True)
    rationale = models.ForeignKey(Rationale, blank=True, default=None, null=True)

    def __str__(self):
        return self.comment

    def __unicode__(self):
        return self.comment


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
    planHardware = models.ManyToManyField(HardwareEquipment, verbose_name='Плановая', related_name="planHardware_name",
                                          blank=True, null=True)
    # внеплановая выдача комплектующих
    noPlanHardware = models.ManyToManyField(HardwareEquipment, verbose_name='Внеплановая',
                                            related_name="no_PlanHardware_name", blank=True, null=True)
    # брак
    rejected = models.ManyToManyField(Reject, blank=True, null=True)
    # выполняемые работы
    workPart = models.ManyToManyField(WorkPart, related_name="work_Part", blank=True, null=True)
    # фактически выполненные работы
    factWorkPart = models.ManyToManyField(WorkPart, related_name="fact_WorkPart", blank=True, null=True)
    # примечание
    note = models.CharField(max_length=10000, default="")

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
                [str(i), wpname, wPart.standartWork.text+" "+wPart.comment, wPart.startTime.strftime("%H:%M"), wPart.endTime.strftime("%H:%M")])

        fwp = []
        i = 0
        for wPart in self.factWorkPart.all().order_by('startTime'):
            i += 1
            if wPart.workPlace is None:
                wpname = "-"
            else:
                wpname = wPart.workPlace.name
            fwp.append(
                [str(i), wpname, wPart.standartWork.text+" "+wPart.comment, wPart.startTime.strftime("%H:%M"), wPart.endTime.strftime("%H:%M")])

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
            #print(e)
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

        print(attestation)
        #print(wp)
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
                if d.get(part.rationle.name):
                    d[part.rationle.name].append(i)
                else:
                    d[part.rationle.name] = [i]
        rationales = []
        for key, value in d.items():
            rationales.append([value, key])
        return rationales

    def __str__(self):
        # return "sad"
        return self.supervisor.getInitials() + "-" + str(self.worker.tnumber) + '-' + str(self.adate)

    def __unicode__(self):
        # return "sad"
        return self.supervisor.getInitials() + "-" + str(self.worker.tnumber) + '-' + str(self.adate)  # класс заказов


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
