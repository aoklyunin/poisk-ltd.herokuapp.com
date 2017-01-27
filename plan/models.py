# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models


# чертёж
class Scheme(models.Model):
    # автор
    author = models.CharField(max_length=200)
    # ссылка
    link = models.CharField(max_length=100)


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
    dimension = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# класс детали
class Equipment(models.Model):
    # название
    name = models.CharField(max_length=1000)
    # материалы
    materials = models.ManyToManyField(Material)
    # чертёж
    scheme = models.ManyToManyField(Scheme)
    # шифр
    code = models.CharField(max_length=100)
    # тип
    hardwareType = models.IntegerField()
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


# рабочее место
class WorkPlace(models.Model):
    # название
    name = models.CharField(max_length=200)


# аттестация
class Attestation(models.Model):
    # название
    name = models.CharField(max_length=200)

    def __str__(self):
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

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


# инструмент
class Instrument(models.Model):
    # название
    name = models.CharField(max_length=200)


# оснаска и комплектующие
class HardwareEquipment(models.Model):
    # название
    name = models.CharField(max_length=200)
    # кол-во
    count = models.FloatField()
    # деталь
    equipment = models.ForeignKey(Equipment)
    # материал
    material = models.ForeignKey(Material)


# брак
class Reject(models.Model):
    # деталь
    equipment = models.ForeignKey(Equipment)
    # кол-во
    cnt = models.IntegerField()


# стандартная работа
class StandartWork(models.Model):
    text = models.CharField(max_length=2000)
    positionsEnable = models.ManyToManyField(WorkerPosition)

    def __str__(self):
        return self.text


# Часть наряда
class WorkPart(models.Model):
    comment = models.CharField(max_length=2000)
    startTime = models.TimeField()
    endTime = models.TimeField()
    standartWork = models.ForeignKey(StandartWork)
    workPlace = models.ForeignKey(WorkPlace, blank=True, default=None)

    def __str__(self):
        return self.name


# наряд
class WorkReport(models.Model):
    # руководитель
    supervisor = models.ForeignKey(Worker, verbose_name='Руководитель', related_name="supervisor_name")
    # ответственный за ВИК
    VIKer = models.ForeignKey(Worker, verbose_name='ВИК', related_name="VIKER_name")
    # исполнитель
    worker = models.ForeignKey(Worker, verbose_name='Иcполнитель', related_name="worker_name")
    # кладовщик
    stockMan = models.ForeignKey(Worker, verbose_name='Кладовщик', related_name="stockMan_name")
    # составитель отчёта
    reportMaker = models.ForeignKey(Worker, verbose_name='Cоставитель отчёта', related_name="reportMaker_name")
    # проверяющий отчёт
    reportChecker = models.ForeignKey(Worker, verbose_name='Проверяющий отчёт', related_name="reportChecker_name")
    # дата
    adate = models.DateField(default=datetime.date.today)
    # дата ВИК
    VIKDate = models.DateField(default=datetime.date.today)
    # плановая выдача комплектующих
    planHardware = models.ManyToManyField(HardwareEquipment, verbose_name='Плановая', related_name="planHardware_name")
    # внеплановая выдача комплектующих
    noPlanHardware = models.ManyToManyField(HardwareEquipment, verbose_name='Внеплановая',
                                            related_name="no_PlanHardware_name")
    # брак
    rejected = models.ManyToManyField(Reject)
    workPart = models.ManyToManyField(WorkPart, related_name="work_Part")
    factWorkPart = models.ManyToManyField(WorkPart, related_name="fact_WorkPart")


# класс заказов
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