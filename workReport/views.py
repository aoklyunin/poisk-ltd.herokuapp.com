# -*- coding: utf-8 -*-
import datetime
import re

from datetime import time
from django.core.checks import messages
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.forms import formset_factory, BaseFormSet
from django.urls import reverse

from plan.forms import LoginForm
from workReport.forms import ReportForm, WorkPartForm, NeedStructForm, RejectForm
from workReport.models import WorkReport, WorkPart, StandartWork, Reject,  Worker, \
    WorkerPosition, NeedStruct


class RequiredFormSet(BaseFormSet):
    def clean(self):
        return

    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


def workReportPage1(request, workReport_id):
    work_report = WorkReport.objects.get(pk=workReport_id)
    # если post запрос
    if request.method == 'POST':
        # строим форму на основе запроса
        form = ReportForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            work_report.supervisor = form.cleaned_data["supervisor"]
            work_report.VIKer = form.cleaned_data["VIKer"]
            work_report.reportMaker = form.cleaned_data["reportMaker"]
            work_report.reportChecker = form.cleaned_data["reportChecker"]
            work_report.worker = form.cleaned_data["worker"]
            work_report.stockMan = form.cleaned_data["stockMan"]
            work_report.adate = form.cleaned_data["adate"]
            work_report.VIKDate = form.cleaned_data["VIKDate"]
            work_report.note = form.cleaned_data["note"]
            work_report.save()
        data = form.cleaned_data
    else:
        data = {'supervisor': work_report.supervisor,
                'VIKer': work_report.VIKer,
                'reportMaker': work_report.reportMaker,
                'reportChecker': work_report.reportChecker,
                'worker': work_report.worker,
                'stockMan': work_report.stockMan,
                'adate': work_report.adate,
                'VIKDate': work_report.VIKDate,
                'note': work_report.note,
                }
    # возвращаем простое окно регистрации
    return render(request, "workReport/workReportPage1.html", {
        'form': ReportForm(initial=data),
        'login_form': LoginForm(),
        'pk': workReport_id,
    })


def workReportPage2(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    ReportFormset = formset_factory(WorkPartForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            wr.workPart.clear()
            for form in report_formset.forms:
                if len(WorkPart.objects.filter(startTime=form.cleaned_data["startTime"],
                                               endTime=form.cleaned_data["endTime"],
                                               standartWork=form.cleaned_data["standartWork"],
                                               workPlace=form.cleaned_data["workPlace"],
                                               rationale=form.cleaned_data["rationale"],
                                               comment=form.cleaned_data["comment"])) > 1:
                    w = WorkPart.objects.filter(startTime=form.cleaned_data["startTime"],
                                                endTime=form.cleaned_data["endTime"],
                                                standartWork=form.cleaned_data["standartWork"],
                                                workPlace=form.cleaned_data["workPlace"],
                                                rationale=form.cleaned_data["rationale"],
                                                comment=form.cleaned_data["comment"]).first()
                else:
                    w, created = WorkPart.objects.get_or_create(startTime=form.cleaned_data["startTime"],
                                                                endTime=form.cleaned_data["endTime"],
                                                                standartWork=form.cleaned_data["standartWork"],
                                                                workPlace=form.cleaned_data["workPlace"],
                                                                rationale=form.cleaned_data["rationale"],
                                                                comment=form.cleaned_data["comment"])
                w.save()
                wr.workPart.add(w)
    else:
        data = {
            'form-TOTAL_FORMS': str(len(wr.workPart.all())),
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': ''
        }
        i = 0
        for part in wr.workPart.all():
            data['form-' + str(i) + '-startTime'] = part.startTime.strftime("%H:%M")
            data['form-' + str(i) + '-endTime'] = part.endTime.strftime("%H:%M")
            data['form-' + str(i) + '-standartWork'] = part.standartWork
            if part.workPlace is not None:
                data['form-' + str(i) + '-workPlace'] = part.workPlace
            if part.rationale is not None:
                data['form-' + str(i) + '-rationale'] = part.rationale
            data['form-' + str(i) + '-comment'] = part.comment
            i += 1
            report_formset = ReportFormset(data)
            #   report_formset.full_clean()
            # report_formset.clean()

    c = {'link_formset': report_formset,
         'login_form': LoginForm(),
         'caption': 'страница 2 - Выполняемые работы',
         'pk': workReport_id,
         }
    return render(request, 'workReport/workReportFormsetWorkPart.html', c)


def workReportPage3(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    ReportFormset = formset_factory(WorkPartForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            wr.factWorkPart.clear()
            for form in report_formset.forms:
                if len(WorkPart.objects.filter(startTime=form.cleaned_data["startTime"],
                                               endTime=form.cleaned_data["endTime"],
                                               standartWork=form.cleaned_data["standartWork"],
                                               workPlace=form.cleaned_data["workPlace"],
                                               rationale=form.cleaned_data["rationale"],
                                               comment=form.cleaned_data["comment"])) > 1:
                    w = WorkPart.objects.filter(startTime=form.cleaned_data["startTime"],
                                                endTime=form.cleaned_data["endTime"],
                                                standartWork=form.cleaned_data["standartWork"],
                                                workPlace=form.cleaned_data["workPlace"],
                                                rationale=form.cleaned_data["rationale"],
                                                comment=form.cleaned_data["comment"]).first()
                else:
                    w, created = WorkPart.objects.get_or_create(startTime=form.cleaned_data["startTime"],
                                                                endTime=form.cleaned_data["endTime"],
                                                                standartWork=form.cleaned_data["standartWork"],
                                                                workPlace=form.cleaned_data["workPlace"],
                                                                rationale=form.cleaned_data["rationale"],
                                                                comment=form.cleaned_data["comment"])
                w.save()
                wr.factWorkPart.add(w)
    else:
        data = {
            'form-TOTAL_FORMS': str(len(wr.factWorkPart.all())),
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': ''
        }
        i = 0
        for part in wr.factWorkPart.all():
            data['form-' + str(i) + '-startTime'] = part.startTime.strftime("%H:%M")
            data['form-' + str(i) + '-endTime'] = part.endTime.strftime("%H:%M")
            data['form-' + str(i) + '-standartWork'] = part.standartWork
            i += 1
        report_formset = ReportFormset(data)
    c = {'link_formset': report_formset,
         'login_form': LoginForm(),
         'caption': 'страница 3 - Фактически выполненные работы',
         'pk': workReport_id,
         }
    return render(request, 'workReport/workReportFormsetWorkPart.html', c)


def calculateEquipment(workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    hw = wr.planHardware
    if not wr.flgCalculateEquipment:
        hw.clear()
        wr.flgCalculateEquipment = True
        for wp in wr.workPart.all():
            for eq in wp.standartWork.hardwareEquipment.all():
                eqg = None
                mtg = None
                if not eq.equipment is None:
                    try:
                        eqg = hw.get(equipment=eq.equipment)
                    except:
                        obj = NeedStruct.objects.get(pk=eq.pk)
                        obj.pk = None
                        obj.save()
                        hw.add(obj)

                if not eq.material is None:
                    try:
                        mtg = hw.get(material=eq.material)
                    except:
                        obj = NeedStruct.objects.get(pk=eq.pk)
                        obj.pk = None
                        obj.save()
                        hw.add(obj)

                if not eqg is None:
                    eqg.getCnt += eq.getCnt
                    eqg.save()
                elif not mtg is None:
                    mtg.getCnt += eq.getCnt
                    mtg.save()

        wr.save()


def workReportPage4(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    ReportFormset = formset_factory(NeedStructForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            wr.planHardware.clear()
            for form in report_formset.forms:
                if (form.cleaned_data["equipment"] is None) and (form.cleaned_data["material"] is None):
                    # print ("empty form line")
                    continue
                if len(NeedStruct.objects.filter(equipment=form.cleaned_data["equipment"],
                                                        material=form.cleaned_data["material"],
                                                        usedCnt=form.cleaned_data["usedCnt"],
                                                        getCnt=form.cleaned_data["getCnt"],
                                                        rejectCnt=form.cleaned_data["rejectCnt"],
                                                        dustCnt=form.cleaned_data["dustCnt"],
                                                        remainCnt=form.cleaned_data["remainCnt"])) > 1:
                    w = NeedStruct.objects.filter(equipment=form.cleaned_data["equipment"],
                                                         material=form.cleaned_data["material"],
                                                         usedCnt=form.cleaned_data["usedCnt"],
                                                         getCnt=form.cleaned_data["getCnt"],
                                                         rejectCnt=form.cleaned_data["rejectCnt"],
                                                         dustCnt=form.cleaned_data["dustCnt"],
                                                         remainCnt=form.cleaned_data["remainCnt"]).first()
                else:
                    w, created = NeedStruct.objects.get_or_create(equipment=form.cleaned_data["equipment"],
                                                                         material=form.cleaned_data["material"],
                                                                         usedCnt=form.cleaned_data["usedCnt"],
                                                                         getCnt=form.cleaned_data["getCnt"],
                                                                         rejectCnt=form.cleaned_data["rejectCnt"],
                                                                         dustCnt=form.cleaned_data["dustCnt"],
                                                                         remainCnt=form.cleaned_data["remainCnt"])
                w.save()
                wr.planHardware.add(w)
    else:
        calculateEquipment(workReport_id)
        if wr.planHardware.all().exists():
            data = {
                'form-TOTAL_FORMS': str(len(wr.planHardware.all())),
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': ''
            }
            i = 0
            for part in wr.planHardware.all():
                data['form-' + str(i) + '-equipment'] = part.equipment
                data['form-' + str(i) + '-material'] = part.material
                data['form-' + str(i) + '-usedCnt'] = part.usedCnt
                data['form-' + str(i) + '-getCnt'] = part.getCnt
                data['form-' + str(i) + '-rejectCnt'] = part.rejectCnt
                data['form-' + str(i) + '-dustCnt'] = part.dustCnt
                data['form-' + str(i) + '-remainCnt'] = part.remainCnt
                i += 1
        else:
            data = {
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
                'form-0-usedCnt': 0.0,
                'form-0-getCnt': 0.0,
                'form-0-rejectCnt': 0.0,
                'form-0-dustCnt': 0.0,
                'form-0-remainCnt': 0.0,
            }
            # print(data)
        report_formset = ReportFormset(data)
        #  print (report_formset)

    c = {'link_formset': report_formset,
         'caption': 'страница 4 - Плановая выдача оборудования',
         'login_form': LoginForm(),
         'pk': workReport_id,
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormsetEquipment.html', c)


def workReportPage5(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)

    #  if wr.workPart.all().exists():
    ReportFormset = formset_factory(NeedStructForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            wr.noPlanHardware.clear()
            for form in report_formset.forms:
                if (form.cleaned_data["equipment"] is None) and (form.cleaned_data["material"] is None):
                    # print ("empty form line")
                    continue
                if len(NeedStruct.objects.filter(equipment=form.cleaned_data["equipment"],
                                                        material=form.cleaned_data["material"],
                                                        usedCnt=form.cleaned_data["usedCnt"],
                                                        getCnt=form.cleaned_data["getCnt"],
                                                        rejectCnt=form.cleaned_data["rejectCnt"],
                                                        dustCnt=form.cleaned_data["dustCnt"],
                                                        remainCnt=form.cleaned_data["remainCnt"])) > 1:
                    w = NeedStruct.objects.filter(equipment=form.cleaned_data["equipment"],
                                                         material=form.cleaned_data["material"],
                                                         usedCnt=form.cleaned_data["usedCnt"],
                                                         getCnt=form.cleaned_data["getCnt"],
                                                         rejectCnt=form.cleaned_data["rejectCnt"],
                                                         dustCnt=form.cleaned_data["dustCnt"],
                                                         remainCnt=form.cleaned_data["remainCnt"]).first()
                else:
                    w, created = NeedStruct.objects.get_or_create(equipment=form.cleaned_data["equipment"],
                                                                         material=form.cleaned_data["material"],
                                                                         usedCnt=form.cleaned_data["usedCnt"],
                                                                         getCnt=form.cleaned_data["getCnt"],
                                                                         rejectCnt=form.cleaned_data["rejectCnt"],
                                                                         dustCnt=form.cleaned_data["dustCnt"],
                                                                         remainCnt=form.cleaned_data["remainCnt"])
                w.save()
                wr.noPlanHardware.add(w)
    else:
        if wr.noPlanHardware.all().exists():
            data = {
                'form-TOTAL_FORMS': str(len(wr.noPlanHardware.all())),
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': ''
            }
            i = 0
            for part in wr.noPlanHardware.all():
                data['form-' + str(i) + '-equipment'] = part.equipment
                data['form-' + str(i) + '-material'] = part.material
                data['form-' + str(i) + '-usedCnt'] = part.usedCnt
                data['form-' + str(i) + '-getCnt'] = part.getCnt
                data['form-' + str(i) + '-rejectCnt'] = part.rejectCnt
                data['form-' + str(i) + '-dustCnt'] = part.dustCnt
                data['form-' + str(i) + '-remainCnt'] = part.remainCnt
                i += 1
        else:
            data = {
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
                'form-0-usedCnt': 0.0,
                'form-0-getCnt': 0.0,
                'form-0-rejectCnt': 0.0,
                'form-0-dustCnt': 0.0,
                'form-0-remainCnt': 0.0,
            }
        report_formset = ReportFormset(data)
    c = {'link_formset': report_formset,
         'caption': 'страница 5 - Внеплановая выдача оборудования',
         'login_form': LoginForm(),
         'pk': workReport_id,
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormsetEquipment.html', c)


def workReportPage6(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)

    #  if wr.workPart.all().exists():
    ReportFormset = formset_factory(RejectForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            wr.rejected.clear()
            for form in report_formset.forms:
                if (form.cleaned_data["equipment"] is None) and (form.cleaned_data["material"] is None):
                    # print ("empty form line")
                    continue
                if len(Reject.objects.filter(equipment=form.cleaned_data["equipment"],
                                             material=form.cleaned_data["material"],
                                             cnt=form.cleaned_data["cnt"])) > 1:
                    w = Reject.objects.filter(equipment=form.cleaned_data["equipment"],
                                              material=form.cleaned_data["material"],
                                              cnt=form.cleaned_data["cnt"]).first()
                else:
                    w, created = Reject.objects.get_or_create(equipment=form.cleaned_data["equipment"],
                                                              material=form.cleaned_data["material"],
                                                              cnt=form.cleaned_data["cnt"])
                w.save()
                wr.rejected.add(w)
    else:
        if wr.rejected.all().exists():
            data = {
                'form-TOTAL_FORMS': str(len(wr.rejected.all())),
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': ''
            }
            i = 0
            for part in wr.rejected.all():
                data['form-' + str(i) + '-equipment'] = part.equipment
                data['form-' + str(i) + '-material'] = part.material
                data['form-' + str(i) + '-cnt'] = part.cnt
                i += 1
        else:
            data = {
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
                'form-0-cnt': 0.0,
            }
        report_formset = ReportFormset(data)
    c = {'link_formset': report_formset,
         'caption': 'страница 6 - Брак',
         'login_form': LoginForm(),
         'pk': workReport_id,
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormsetRejected.html', c)



def workReports(request):
    return render(request, 'workReport/workReportList.html',
                  {'reports':
                       WorkReport.objects.all().order_by('-adate')
                   })


def createWorkReport(request):
    w = WorkReport()
    wPos = WorkerPosition.objects.get(name='Контролёр ОТК')
    w.VIKer = Worker.objects.filter(position=wPos).first()
    w.reportMaker = Worker.objects.all().first()
    w.reportChecker = Worker.objects.all().first()
    w.worker = Worker.objects.all().first()
    wPos = WorkerPosition.objects.get(name='Начальник смены')
    w.supervisor = Worker.objects.filter(position=wPos).first()
    wPos = WorkerPosition.objects.get(name='Кладовщик')
    w.stockMan = Worker.objects.filter(position=wPos).first()
    w.save()
    # заявленные работы
    wp = WorkPart.objects.create(startTime=time(hour=8, minute=30),
                                 endTime=time(hour=8, minute=45),
                                 standartWork=StandartWork.objects.get(
                                     text='Получение наряда и ТМЦ для выполнения работ'),
                                 )
    w.workPart.add(wp)
    wp = WorkPart.objects.create(startTime=time(hour=16, minute=45),
                                 endTime=time(hour=17, minute=00),
                                 standartWork=StandartWork.objects.get(text='Уборка рабочего места'),
                                 )
    w.workPart.add(wp)
    # фактически выполненные работы
    wp = WorkPart.objects.create(startTime=time(hour=8, minute=30),
                                 endTime=time(hour=8, minute=45),
                                 standartWork=StandartWork.objects.get(
                                     text='Получение наряда и ТМЦ для выполнения работ'),
                                 )
    w.factWorkPart.add(wp)
    wp = WorkPart.objects.create(startTime=time(hour=16, minute=30),
                                 endTime=time(hour=16, minute=45),
                                 standartWork=StandartWork.objects.get(
                                     text='Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий день, проверка инструмента, сдача ТМЦ'),
                                 )
    w.factWorkPart.add(wp)

    wp = WorkPart.objects.create(startTime=time(hour=16, minute=45),
                                 endTime=time(hour=17, minute=00),
                                 standartWork=StandartWork.objects.get(
                                     text='Уборка рабочего места'),
                                 )
    w.factWorkPart.add(wp)

    return HttpResponseRedirect('/workReport/page1/' + str(w.pk) + '/')


def deleteReport(request, workReport_id):
    WorkReport.objects.filter(pk=workReport_id).delete()
    return HttpResponseRedirect('/workReport/list/')


def printReport(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    document = wr.generateDoc()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=report.docx'
    document.save(response)

    return response
