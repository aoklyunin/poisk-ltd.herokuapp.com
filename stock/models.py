# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.db import models

from plan.models import Area






class MoveEquipment(models.Model):
    date = models.DateField(default=datetime.date.today)
    cnt = models.IntegerField(default=0)
    equipment = models.ForeignKey("constructors.Equipment")
    flgAcceptance = models.BooleanField(default=True)
    remainCnt = models.IntegerField(default=0)

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


class MoveStandartWork(models.Model):
    date = models.DateField(default=datetime.date.today)
    cnt = models.IntegerField(default=0)
    standartWork = models.ForeignKey("constructors.StandartWork", blank=True, null=True)
    flgAcceptance = models.BooleanField(default=True)
    remainCnt = models.IntegerField(default=0)

    def __str__(self):
        return str(self.standartWork) + ":" + str(self.cnt)
