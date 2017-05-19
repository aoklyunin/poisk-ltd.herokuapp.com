# -*- coding: utf-8 -*-
import datetime
import time
from django.db import models

from constructors.models import NeedStruct, Equipment, Scheme
#from nop.models import WorkPlace
from nop.models import WorkPlace, Area, Worker
from orders.models import Order
from plan.models import Agreement, WorkerPosition, Rationale

from plan.models import Customer
from stock.models import MoveEquipment
from workReport.workReportGenerator import generateReport


# сколько по складу
class StockReportStruct(models.Model):
    # оборудование
    equipment = models.ForeignKey('constructors.Equipment', blank=True)
    # должно быть выдано
    cnt = models.FloatField(default=0)
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
    # состояние нарада
    state = models.IntegerField(default=0)

    STATE_CREATED = 0
    STATE_STOCK_READY = 1
    STATE_GETTED_FROM_STOCK = 2
    STATE_LEAVED_TO_STOCK = 3
    STATE_CLOSED = 4
    STATE_OTK_ACCEPTED = 5

    def genfactWorkPart(self):
        for wp in self.workPart.all():
            self.factWorkPart.add(wp)

    def generateAcceptanceData(self):
        arr = []
        for ph in self.planHardware.all().order_by('equipment'):
            arr.append({
                'cnt': ph.cnt,
                'equipment': ph.equipment.name,
                'ss': ph,
                'rejectCnt': ph.rejectCnt,
                'dustCnt': ph.dustCnt,
                'returnCnt': ph.returnCnt,
            })
        for ph in self.noPlanHardware.all().order_by('equipment'):
            arr.append({
                'cnt': ph.cnt,
                'equipment': ph.equipment.name,
                'ss': ph,
                'rejectCnt': ph.rejectCnt,
                'dustCnt': ph.dustCnt,
                'returnCnt': ph.returnCnt,
            })
        return arr


    def processAcceptanceFormset(self, formset, area_id):
        # без вывода почему-то выдаёт ошибку, что не может обратиться к cleaned_data
        if formset.is_valid:
            for form in formset.forms:
                if form.is_valid:
                    d = form.cleaned_data
                    if 'ss' in d:
                        # print(form.cleaned_data)
                        ss = d['ss']
                        ss.rejectCnt = d["rejectCnt"]
                        ss.dustCnt = d["dustCnt"]
                        ss.returnCnt = d["returnCnt"]
                        ss.save()
                        e = MoveEquipment.objects.create(
                            equipment=ss.equipment,
                            cnt=ss.returnCnt,
                            flgAcceptance=True,
                        )
                        e.save()
                        e.acceptMoving(area_id)

            self.state = self.STATE_LEAVED_TO_STOCK
            self.save()

    def extraditionEquipment(self):
        for e in self.planHardware.all():
            if (e.cnt is not None):
                e = MoveEquipment.objects.create(
                    equipment=e.equipment,
                    cnt=e.cnt,
                    flgAcceptance=False,
                )
                e.save()
                e.acceptMoving(self.area)
        for e in self.noPlanHardware.all():
            if (e.cnt is not None):
                e = MoveEquipment.objects.create(
                    equipment=e.equipment,
                    cnt=e.cnt,
                    flgAcceptance=False,
                )
                e.save()
                e.acceptMoving(self.area)
        self.state = self.STATE_GETTED_FROM_STOCK
        self.save()

    # сохранить внеплановое оборудование
    def saveNoPlanHardware(self, formset):
        if formset.is_valid():
            self.noPlanHardware.clear()
            for form in formset.forms:
                if form.is_valid:
                    d = form.cleaned_data
                    if (len(d) > 0) and ("cnt" in d) and (float(d["cnt"]) > 0) and \
                            (("equipment" in d) and (not d["equipment"] is None) and (d["equipment"] != self)):
                        print(d)
                        ss = StockReportStruct.objects.create(equipment=Equipment.objects.get(pk=int(d["equipment"])),
                                                              cnt=float(d["cnt"]))
                        ss.save()
                        self.noPlanHardware.add(ss)
                else:
                    print("for is not valid")

    # список планового оборудования
    def generatePlanHardwareVals(self):
        arr = []
        for ns in self.planHardware.all():
            if (ns.equipment != None):
                print(self.area)
                arr.append({'equipment': ns.equipment,
                            'cnt': ns.cnt}
                           )
        return arr

    # список всего оборудования с указание остатка на складе
    def generateHardwareVals(self):
        pE = self.generatePlanHardwareVals()
        nPE = self.generateNonPlanHardwareVals()
        d = {}
        for e in pE:
            d[e["equipment"]] = {
                "plan": e["cnt"],
                "nonPlan": 0
            }

        for e in nPE:
            if e["equipment"] in d:
                d[e["equipment"]]["nonPlan"] = e["cnt"]
            else:
                d[e["equipment"]] = {
                    "plan": 0,
                    "nonPlan": e["cnt"]
                }
        arr = []
        for key, value in d.items():
            tmp = {
                "equipment": key,
                "plan": d[key]["plan"],
                "nonPlan": d[key]["nonPlan"],
            }
            tmp["remain"] = key.stockStruct.get(area=Area.objects.get(pk=self.area)).cnt
            tmp["sum"] = d[key]["plan"] + d[key]["nonPlan"]
            arr.append(tmp)

        return arr

    # список внепланового оборудования
    def generateNonPlanHardwareVals(self):
        arr = []
        for ns in self.noPlanHardware.all():
            if (ns.equipment != None):
                arr.append({'equipment': ns.equipment,
                            'cnt': ns.cnt,
                            })
        return arr

    # список внепланового оборудования
    def generateNonPlanHardware(self):
        arr = []
        for ns in self.noPlanHardware.all():
            if (ns.equipment != None):
                arr.append({'equipment': str(ns.equipment.pk),
                            'cnt': str(ns.cnt)})
        return arr

    # сохранить стандартные работы
    def saveWorkPartFromFormset(formset, workPart):
        workPart.clear()
        for form in formset.forms:
            try:
                d = form.cleaned_data
                if (len(d) > 0) and ("standartWork" in d) and (not d["standartWork"] is None) and \
                        (form.cleaned_data["standartWork"] != ""):

                    sw = Equipment.objects.get(pk=int(form.cleaned_data["standartWork"]))
                    if form.cleaned_data["workPlace"] == "":
                        wp = None
                    else:
                        wp = WorkPlace.objects.get(pk=int(form.cleaned_data["workPlace"]))

                    if form.cleaned_data["rationale"] == "":
                        r = None
                    else:
                        r = Rationale.objects.get(pk=int(form.cleaned_data["rationale"]))

                    if len(WorkPart.objects.filter(startTime=form.cleaned_data["startTime"],
                                                   endTime=form.cleaned_data["endTime"],
                                                   standartWork=sw,
                                                   workPlace=wp,
                                                   rationale=r,
                                                   comment=form.cleaned_data["comment"])) > 1:
                        w = WorkPart.objects.filter(startTime=form.cleaned_data["startTime"],
                                                    endTime=form.cleaned_data["endTime"],
                                                    standartWork=sw,
                                                    workPlace=wp,
                                                    rationale=r,
                                                    comment=form.cleaned_data["comment"]).first()
                    else:
                        w, created = WorkPart.objects.get_or_create(startTime=form.cleaned_data["startTime"],
                                                                    endTime=form.cleaned_data["endTime"],
                                                                    standartWork=sw,
                                                                    workPlace=wp,
                                                                    rationale=r,
                                                                    comment=form.cleaned_data["comment"])
                    w.save()
                    workPart.add(w)
            except:
                print("def saveWorkPartFromFormset: Ошибка чтения формы " + str(form))

    # получить основные данные отчёта
    def getMainReportData(self):
        return {
            'supervisor': self.supervisor,
            'VIKer': self.VIKer,
            'reportMaker': self.reportMaker,
            'reportChecker': self.reportChecker,
            'worker': self.worker,
            'stockMan': self.stockMan,
            'adate': self.adate,
            'VIKDate': self.VIKDate,
            'note': self.note,
            'area': self.area,
        }

    # генерируем планируемые работы
    def generateFactWorkPartData(self):
        # member_data = list(self.workPart.all().values())
        # return list(member_data)
        arr = []
        for wp in self.factWorkPart.all().order_by('startTime'):
            if wp.workPlace is None:
                strWorkPlace = ""
            else:
                strWorkPlace = str(wp.workPlace.pk)

            if wp.rationale is None:
                strRationale = ""
            else:
                strRationale = str(wp.rationale.pk)

            arr.append({
                'comment': str(wp.comment),
                'startTime': wp.startTime,
                'endTime': wp.endTime,
                'standartWork': str(wp.standartWork.pk),
                'workPlace': strWorkPlace,
                'rationale': strRationale,
            })
        return arr

    # генерируем фактически выполненные работы
    def generateWorkPartData(self):
        # member_data = list(self.workPart.all().values())
        # return list(member_data)
        arr = []
        for wp in self.workPart.all().order_by('startTime'):
            if wp.workPlace is None:
                strWorkPlace = ""
            else:
                strWorkPlace = str(wp.workPlace.pk)

            if wp.rationale is None:
                strRationale = ""
            else:
                strRationale = str(wp.rationale.pk)

            arr.append({
                'comment': str(wp.comment),
                'startTime': wp.startTime,
                'endTime': wp.endTime,
                'standartWork': str(wp.standartWork.pk),
                'workPlace': strWorkPlace,
                'rationale': strRationale,
            })
        return arr

    # генерируем отчёт
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
                [str(i), wpname, wPart.standartWork.name + " " + wPart.comment, wPart.startTime.strftime("%H:%M"),
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
                [str(i), wpname, wPart.standartWork.name + " " + wPart.comment, wPart.startTime.strftime("%H:%M"),
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
            for l in [str(equip.cnt), str(equip.cnt - equip.returnCnt), str(equip.rejectCnt), str(equip.dustCnt),
                      str(equip.returnCnt)]:
                e.append(l)
            planEquipment.append(e)

        nonPlanEquipment = []
        for equip in self.noPlanHardware.all():
            e = []
            if equip.equipment is None:
                e = [equip.material.name, equip.material.code, equip.material.dimension]
            else:
                e = [equip.equipment.name, equip.equipment.code, equip.equipment.dimension]
            for l in [str(equip.cnt), str(equip.cnt - equip.returnCnt), str(equip.rejectCnt), str(equip.dustCnt),
                      str(equip.returnCnt)]:
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
