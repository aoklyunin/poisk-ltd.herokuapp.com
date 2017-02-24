# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# оснаска и комплектующие
from mysite import settings
from workReport.workReportGenerator import generateReport


class Scheme(models.Model):
    # автор
    author = models.CharField(max_length=200)
    # ссылка
    link = models.CharField(max_length=100)

    def __unicode__(self):
        return self.author

    def __str__(self):
        return self.author


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
        s = ""
        for pos in self.position.all():
            s += str(pos) + ", "
        return str(self.tnumber) + " - " + self.getShort() + "(" + s[:-2] + ")"

    def __unicode__(self):
        return str(self.tnumber) + " - "+self.getShort()


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

    def __str__(self):
        if self.material is None:
            print(self.equipment.name + " " + str(self.getCnt) + " " + self.equipment.dimension)
            return self.equipment.name + " " + str(self.getCnt) + " " + self.equipment.dimension
        else:
            return self.material.name + " " + str(self.getCnt) + " " + self.material.dimension

    def __unicode__(self):
        if self.material is None:
            return self.equipment.name + " " + str(self.getCnt) + " " + self.equipment.dimension
        else:
            return self.material.name + " " + str(self.getCnt) + " " + self.material.dimension


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
    hardwareEquipment = models.ManyToManyField(HardwareEquipment, blank=True, default=None, null=True)
    duration = models.FloatField(default=0)

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

    def __str__(self):
        return self.startTime.strftime("%H:%M") + "-" + self.endTime.strftime("%H:%M") + " " \
               + str(self.standartWork) + " " + self.comment

    def __unicode__(self):
        return self.startTime.strftime("%H:%M") + "-" + self.endTime.strftime("%H:%M") + " " + str(
            self.standartWork) + " " + self.comment


class UserLink(models.Model):
    user = models.OneToOneField(User)
    anchor = models.CharField(max_length=100)
    url = models.URLField()


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
    note = models.CharField(max_length=10000, default="", blank=True, null=True)

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
