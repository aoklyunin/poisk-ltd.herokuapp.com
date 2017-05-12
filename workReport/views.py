# -*- coding: utf-8 -*-
import datetime
import re
import os
import sys
import urllib

from datetime import time
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.forms import formset_factory, BaseFormSet

from constructors.form import EquipmentSingleWithCtnForm, EquipmentListWithoutSWForm, EquipmentCntWithoutSWForm
from constructors.models import Equipment
from mysite import settings
from plan.forms import LoginForm, RequiredFormSet
from plan.models import Area, InfoText, WorkPlace, Rationale
from workReport.forms import ReportForm, WorkPartForm, NeedStructForm, RejectForm, CreatedReportSingleForm, \
    CloseReportSingleForm
from workReport.models import WorkReport, WorkPart, Reject, Worker, \
    WorkerPosition, NeedStruct, StockReportStruct


# главная страница раздела нарядов


def index(request):
    c = {
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="workReport_index")
    }
    return render(request, "workReport/index.html", c)


# главная страница раздела нарядов
def formReport(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = CreatedReportSingleForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            return HttpResponseRedirect("/workReport/detailCratedWorkReport/" + form.cleaned_data["report"] + "/")

    c = {
        'login_form': LoginForm(),
        'reportForm': CreatedReportSingleForm(),
    }
    return render(request, "workReport/formReport.html", c)


# редактирование созданного наряда
def detailCratedWorkReport(request, workReport_id):
    work_report = WorkReport.objects.get(pk=workReport_id)
    ReportFormset = formset_factory(WorkPartForm)
    # если post запрос
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES, prefix="formset")
        #   print(report_formset)
        if report_formset.is_valid():
            # print(report_formset)
            WorkReport.saveWorkPartFromFormset(report_formset, work_report.workPart)

        # обработка данных о наряде
        form = ReportForm(request.POST, prefix="reportForm")
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
            #  print(form.cleaned_data["area"].pk)
            work_report.area = form.cleaned_data["area"].pk
            work_report.save()

    c = {
        'form': ReportForm(initial=work_report.getMainReportData(), prefix="reportForm"),
        'login_form': LoginForm(),
        'pk': workReport_id,
        'link_formset': ReportFormset(initial=work_report.generateWorkPartData(), prefix="formset"),
    }

    return render(request, "workReport/detailCratedWorkReport.html", c)


# создать наряд
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
    w.area = Area.objects.first().pk
    w.save()

    # заявленные работы
    wp = WorkPart.objects.create(startTime=time(hour=8, minute=30),
                                 endTime=time(hour=8, minute=45),
                                 standartWork=Equipment.objects.get(
                                     name='Получение наряда и ТМЦ для выполнения работ'),
                                 )
    w.workPart.add(wp)
    wp = WorkPart.objects.create(startTime=time(hour=16, minute=45),
                                 endTime=time(hour=17, minute=00),
                                 standartWork=Equipment.objects.get(name='Уборка рабочего места'),
                                 )
    w.workPart.add(wp)
    # фактически выполненные работы
    wp = WorkPart.objects.create(startTime=time(hour=8, minute=30),
                                 endTime=time(hour=8, minute=45),
                                 standartWork=Equipment.objects.get(
                                     name='Получение наряда и ТМЦ для выполнения работ'),
                                 )
    w.factWorkPart.add(wp)
    wp = WorkPart.objects.create(startTime=time(hour=16, minute=30),
                                 endTime=time(hour=16, minute=45),
                                 standartWork=Equipment.objects.get(
                                     name='Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий день, проверка инструмента, сдача ТМЦ'),
                                 )
    w.factWorkPart.add(wp)

    wp = WorkPart.objects.create(startTime=time(hour=16, minute=45),
                                 endTime=time(hour=17, minute=00),
                                 standartWork=Equipment.objects.get(
                                     name='Уборка рабочего места'),
                                 )
    w.factWorkPart.add(wp)

    return HttpResponseRedirect('/workReport/detailCratedWorkReport/' + str(w.pk) + '/')


# выдача оборудования
def equipment(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = CreatedReportSingleForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            return HttpResponseRedirect("/workReport/detailEquipmentWorkReport/" + form.cleaned_data["report"] + "/")

    c = {
        'login_form': LoginForm(),
        'reportForm': CreatedReportSingleForm(),
    }
    return render(request, "workReport/equipment.html", c)


# редактирование созданного наряда
def detailEquipmentWorkReport(request, workReport_id):
    work_report = WorkReport.objects.get(pk=workReport_id)
    EquipmentFormset = formset_factory(EquipmentCntWithoutSWForm)

    # если post запрос
    if request.method == 'POST':
        report_formset = EquipmentFormset(request.POST, request.FILES, prefix="equipment")
        # print(report_formset)
        if report_formset.is_valid():
            # print(report_formset)
            work_report.saveNoPlanHardware(report_formset)

    c = {
        'factEquipments': work_report.planHardware.all(),
        'standartWorks': work_report.workPart.all(),
        'workReport_id': workReport_id,
        'login_form': LoginForm(),
        'pk': workReport_id,
        'flgCalculate': work_report.flgCalculateEquipment,
        'link_formset': EquipmentFormset(initial=work_report.generateNonPlanHardware(), prefix='equipment')
    }

    return render(request, "workReport/detailEquipmentWorkReport.html", c)


# посчитать плановую выдачу оборудования
def calculateEquipment(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    d = {}
    for wp in wr.workPart.all():
        for ns in wp.standartWork.needStruct.all().exclude(equipment__equipmentType=Equipment.TYPE_STANDART_WORK):
            if ns.equipment in d:
                d[ns.equipment] += ns.cnt
            else:
                d[ns.equipment] = ns.cnt

    hw = wr.planHardware
    hw.clear()
    for key, value in d.items():
        s = StockReportStruct.objects.create(equipment=key, cnt=value)
        s.save()
        hw.add(s)

    wr.flgCalculateEquipment = True
    wr.save()
    return HttpResponseRedirect("/workReport/detailEquipmentWorkReport/" + workReport_id + "/")


# главная страница раздела нарядов
def stockReady(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    if wr.flgCalculateEquipment:
        wr.state = WorkReport.STATE_STOCK_READY
        wr.save()

    return HttpResponseRedirect("/workReport/equipment/")


# главная страница раздела нарядов
def closeReport(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = CloseReportSingleForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            return HttpResponseRedirect("/workReport/detailCloseWorkReport/" + form.cleaned_data["report"] + "/")

    c = {
        'login_form': LoginForm(),
        'reportForm': CloseReportSingleForm(),
    }
    return render(request, "workReport/closeReport.html", c)


# главная страница раздела нарядов
def doCloseReport(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    print(wr)
    return HttpResponseRedirect("/workReport/closeReport/")


# редактирование созданного наряда
def detailCloseWorkReport(request, workReport_id):
    work_report = WorkReport.objects.get(pk=workReport_id)
    ReportFormset = formset_factory(WorkPartForm)
    # если post запрос
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES, prefix="formset")
        #   print(report_formset)
        if report_formset.is_valid():
            # print(report_formset)
            WorkReport.saveWorkPartFromFormset(report_formset, work_report.factWorkPart)

    c = {
        'login_form': LoginForm(),
        'pk': workReport_id,
        'workReport_id': workReport_id,
        'link_formset': ReportFormset(initial=work_report.generateFactWorkPartData(), prefix="formset"),
    }

    return render(request, "workReport/detailCloseWorkReport.html", c)


# главная страница раздела нарядов
def otk(request):
    c = {
        'area_id': Area.objects.first().pk,
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="workReport_index")
    }
    return render(request, "workReport/otk.html", c)


# главная страница раздела нарядов
def archive(request):
    c = {
        'area_id': Area.objects.first().pk,
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="workReport_index")
    }
    return render(request, "workReport/otk.html", c)


def deleteReport(request, workReport_id):
    WorkReport.objects.filter(pk=workReport_id).delete()
    return HttpResponseRedirect('/workReport/list/0/')


def printReport(request, tp, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    document = wr.generateDoc()
    if int(tp) == 0:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        original_filename = str(wr)+u".doc"
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename.encode('utf-8'))
        response['Content-Disposition'] = "attachment; "+filename_header
        document.save(response)
        return response
    else:
        tmpPath = str(settings.PROJECT_ROOT) + "\\tempFiles\\"
        document.save(tmpPath + "t.docx")
        command = 'unoconv --format pdf ' + tmpPath + 't.docx'
        print(command)
        os.system(command)
        test_file = open(tmpPath + "t.pdf", 'rb')
        response = HttpResponse(content=test_file)
        response['Content-Type'] = 'application/pdf'
        original_filename = str(wr) + u".pdf"
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename.encode('utf-8'))
        response['Content-Disposition'] = "attachment; " + filename_header
        return response

       # if (str(sys.platform)=="win32") or (str(sys.platform)=="win64"):
            #pythoncom.CoInitialize()
            #word = client.DispatchEx("Word.Application")
            #worddoc = word.Documents.Open(tmpPath+"tmp.docx")
            #worddoc.SaveAs(tmpPath+"tmp.pdf", FileFormat=17)
            #worddoc.Close()
            #test_file = open(tmpPath+"tmp.pdf", 'rb')
            #response = HttpResponse()
            #response['Content-Type'] = 'application/pdf'
            # original_filename = str(wr) + u".pdf"
            #  filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename.encode('utf-8'))
            # response['Content-Disposition'] = "attachment; " + filename_header
           # return response
        #else:


        # original_filename = str(wr) + u".pdf"
        #  filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(original_filename.encode('utf-8'))
        # response['Content-Disposition'] = "attachment; " + filename_header
