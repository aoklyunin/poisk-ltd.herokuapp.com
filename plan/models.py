# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models


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


# договор
class Agreement(models.Model):
    # ссылка на договор
    link = models.CharField(max_length=1000)

    def __str__(self):
        return self.link

    def __unicode__(self):
        return self.link


class WorkerPosition(models.Model):
    # название
    name = models.CharField(max_length=200)

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
        return self.name + "(" + self.contactPerson + ")"

    def __unicode__(self):
        return self.name + "(" + self.contactPerson + ")"


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
        return str(self.tnumber) + " - " + self.getShort()


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


# обоснование для работы
class Rationale(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# площадка
class Area(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
