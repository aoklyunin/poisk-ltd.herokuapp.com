# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


# аттестация
class Attestation(models.Model):
    # название
    name = models.CharField(max_length=200)

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

# площадка
class Area(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name



class WorkPlace(models.Model):
    # название
    name = models.CharField(max_length=200)
    # цех
    department = models.IntegerField(default=1)
    # участок
    sector = models.IntegerField(default=1)
    # рабочее место
    number = models.IntegerField(default=1)
    # аттестации
    attestations = models.ManyToManyField(Attestation, null=True, blank=True)
    # должности допускаемые на это рабочее место
    wpos = models.ManyToManyField(WorkerPosition)
    # площадка
    area = models.ForeignKey(Area, blank=True,default=None,null=True)

    def __unicode__(self):
        return str(self.department) + "." + str(self.sector) + "." + str(self.number) + " " + self.name

    def __str__(self):
        return str(self.department) + "." + str(self.sector) + "." + str(self.number) + " " + self.name



# работник
class Worker(models.Model):
    # должность
    position = models.ManyToManyField(WorkerPosition, blank=True)
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
    # площадка по умолчанию
    area = models.ForeignKey(Area, blank=True, default=None, null=True)

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
