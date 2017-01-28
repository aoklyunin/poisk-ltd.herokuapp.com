# -*- coding: utf-8 -*-
import datetime
import os
from audioop import reverse
from io import StringIO

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db import transaction
from django.forms import formset_factory, modelformset_factory, BaseFormSet
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.contrib import messages
# Create your views here.
from django import forms;
from django.template import RequestContext
from django.template.context_processors import csrf

from mysite import settings
from plan.forms import ReportForm, LoginForm, WorkPartForm, HardwareEquipmentForm, RejectForm
from plan.models import Worker, WorkReport, WorkPart, StandartWork, HardwareEquipment, Reject
from plan.workReportGenerator import generateReport


def generateWorkReport(request):
    rationales = [
        ['2,3', 'Я так захотел'],
        ['3,4,5', 'А это заставили']
    ]
    works = [
        ['1', '-', 'Получение наряда и ТМЦ для выполнения работ', '08:30', '08:45'],
        ['2', '1.2.3', 'Изготовление деталей оснастки для сушки лейнеров по прилагаемому чертежу в кол-ве одного '
                       'комплекта', '13:15', '16:15'],
        ['3', '-', 'Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий день,'
                   'проверка инструмента, сдача ТМЦ', '16:15', '16:45'],
        ['4', '1.2.3', 'Уборка рабочего места', '16:45', '17:00'],
    ]

    factWorks = [
        ['1', '-', 'Получение наряда и ТМЦ для выполнения работ', '08:30', '08:45'],
        ['2', '1.2.3', 'Изготовление деталей оснастки для сушки лейнеров по прилагаемому чертежу в кол-ве одного '
                       'комплекта', '13:15', '16:15'],
        ['3', '-', 'Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий'
                   'день, проверка инструмента, сдача ТМЦ ', '16:15', '16:45'],
        ['4', '1.2.3', 'Уборка рабочего места', '16:45', '17:00'],
    ]
    note = '''Примечание 1 (обязательное):
    Максимальный срок проведения ВИК (входного контроля) до конца рабочего дня 16.01.2017 г.'''

    planEquipment = [
        ['Перчатки х/б', '123', 'пара', '1', '0', '0', '0', '-1'],
        ['Пруток бронза', 'Б132r', 'мм', '200', '0', '0', '0', '-1'],
    ]
    nonPlanEquipment = [
        ['asf х/б', '123', 'пара', '1', '0', '0', '0', '-1'],
        ['Пруток бронза', 'Б132r', 'мм', '200', '1', '2', '1', '5'],
    ]
    dust = [
        ['хлам 1', '100'],
        ['хлам 2', '500']
    ]

    document = generateReport('ШАВ', 'Шанин А.В.', 'Бука А.В', '124', "Головнёв А.К.", datetime.date.today(), 'Токарь',
                              rationales, works, factWorks, 'Шанин А.В.', 'Шанин А.В.', 'Хионин Б.Г.', note,
                              'аттестация отутствует', dust, planEquipment, nonPlanEquipment)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=report.docx'
    document.save(response)

    return response


def workReportPage1(request, workReport_id):
    # если post запрос
    if request.method == 'POST':
        # строим форму на основе запроса
        form = ReportForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            work_report = WorkReport.objects.get(pk=workReport_id)
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

            # возвращаем простое окно регистрации
            return HttpResponseRedirect('/workReport/page2/' + str(work_report.pk) + '/')
        else:
            data = {'supervisor': form.cleaned_data["supervisor"],
                    'VIKer': form.cleaned_data["VIKer"],
                    'reportMaker': form.cleaned_data["reportMaker"],
                    'reportChecker': form.cleaned_data["reportChecker"],
                    'worker': form.cleaned_data["worker"],
                    'stockMan': form.cleaned_data["stockMan"],
                    'date': form.cleaned_data["date"],
                    'note': form.cleaned_data["note"],
                    }
            return render(request, "plan/workReportPage1.html", {
                'form': ReportForm(data),
                'login_form': LoginForm()
            })
    else:
        # возвращаем простое окно регистрации
        return render(request, "plan/workReportPage1.html", {
            'form': ReportForm(),
            'login_form': LoginForm()
        })


def workReportPage2(request, workReport_id):
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    wr = WorkReport.objects.get(pk=workReport_id)

    #  if wr.workPart.all().exists():

    ReportFormset = formset_factory(WorkPartForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.workPart.all().exists():
                wr.workPart.all().delete()
            for form in report_formset.forms:
                w = WorkPart.objects.create(startTime=form.cleaned_data["startTime"],
                                            endTime=form.cleaned_data["endTime"],
                                            standartWork=form.cleaned_data["standartWork"],
                                            workPlace=None,
                                            rationale=None)
                w.save()
                wr.workPart.add(w)
                print (form.cleaned_data)
            return HttpResponseRedirect('/workReport/page3/' + str(workReport_id) + '/')
    else:
        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-startTime': '08:30',
            'form-0-endTime': '08:45',
            'form-1-startTime': '16:45',
            'form-1-endTime': '17:00',
            'form-0-standartWork': StandartWork.objects.get(text='Получение наряда и ТМЦ для выполнения работ'),
            'form-1-standartWork': StandartWork.objects.get(text='Уборка рабочего места')
        }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Выполняемые работы'
         }
    #  c.update(csrf(request))
    return render(request, 'plan/workReportFormset.html', c)


def workReportPage3(request, workReport_id):
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    wr = WorkReport.objects.get(pk=workReport_id)

    #  if wr.workPart.all().exists():

    ReportFormset = formset_factory(WorkPartForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.factWorkPart.all().exists():
                wr.factWorkPart.all().delete()
            for form in report_formset.forms:
                w = WorkPart.objects.create(startTime=form.cleaned_data["startTime"],
                                            endTime=form.cleaned_data["endTime"],
                                            standartWork=form.cleaned_data["standartWork"],
                                            workPlace=None,
                                            rationale=None)
                w.save()
                wr.factWorkPart.add(w)
                print (form.cleaned_data)
            return HttpResponseRedirect('/workReport/page4/' + str(workReport_id) + '/')
    else:
        data = {
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
            'form-0-startTime': '08:30',
            'form-0-endTime': '08:45',
            'form-1-startTime': '16:30',
            'form-1-endTime': '16:45',
            'form-2-startTime': '16:45',
            'form-2-endTime': '17:00',
            'form-0-standartWork': StandartWork.objects.get(text='Получение наряда и ТМЦ для выполнения работ'),
            'form-1-standartWork': StandartWork.objects.get(
                text='Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий день, проверка инструмента, сдача ТМЦ'),
            'form-2-standartWork': StandartWork.objects.get(text='Уборка рабочего места')
        }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Фактически выполненные работы'
         }
    #  c.update(csrf(request))
    return render(request, 'plan/workReportFormset.html', c)


def workReportPage4(request, workReport_id):
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    wr = WorkReport.objects.get(pk=workReport_id)


    #  if wr.workPart.all().exists():

    ReportFormset = formset_factory(HardwareEquipmentForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.planHardware.all().exists():
                wr.planHardware.all().delete()
            for form in report_formset.forms:
                w = HardwareEquipment.objects.create(
                    # деталь
                    equipment=form.cleaned_data["equipment"],
                    material=form.cleaned_data["material"],
                    usedCnt=form.cleaned_data["usedCnt"],
                    getCnt=form.cleaned_data["getCnt"],
                    rejectCnt=form.cleaned_data["rejectCnt"],
                    dustCnt=form.cleaned_data["dustCnt"],
                    remainCnt=form.cleaned_data["remainCnt"]
                )
                w.save()
                wr.planHardware.add(w)
                print (form.cleaned_data)
            return HttpResponseRedirect('/workReport/page5/' + str(workReport_id) + '/')
    else:
        data = {
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Плановая выдача оборудования'
         }
    #  c.update(csrf(request))
    return render(request, 'plan/workReportFormset.html', c)


def workReportPage5(request, workReport_id):
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    wr = WorkReport.objects.get(pk=workReport_id)

    #  if wr.workPart.all().exists():

    ReportFormset = formset_factory(HardwareEquipmentForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.noPlanHardware.all().exists():
                wr.noPlanHardware.all().delete()
            for form in report_formset.forms:
                w = HardwareEquipment.objects.create(
                    # деталь
                    equipment=form.cleaned_data["equipment"],
                    material=form.cleaned_data["material"],
                    usedCnt=form.cleaned_data["usedCnt"],
                    getCnt=form.cleaned_data["getCnt"],
                    rejectCnt=form.cleaned_data["rejectCnt"],
                    dustCnt=form.cleaned_data["dustCnt"],
                    remainCnt=form.cleaned_data["remainCnt"]
                )
                w.save()
                wr.noPlanHardware.add(w)
                print (form.cleaned_data)
            return HttpResponseRedirect('/workReport/page6/' + str(workReport_id) + '/')
    else:
        data = {
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Внеплановая выдача оборудования'
         }
    #  c.update(csrf(request))
    return render(request, 'plan/workReportFormset.html', c)


def workReportPage6(request, workReport_id):
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    wr = WorkReport.objects.get(pk=workReport_id)

    #  if wr.workPart.all().exists():

    ReportFormset = formset_factory(RejectForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.rejected.all().exists():
                wr.rejected.all().delete()
            for form in report_formset.forms:
                w = Reject.objects.create(
                    # деталь
                    equipment=form.cleaned_data["equipment"],
                    material=form.cleaned_data["material"],
                    cnt=form.cleaned_data["cnt"],
                )
                w.save()
                wr.rejected.add(w)
                print (form.cleaned_data)
            return HttpResponseRedirect('/workReport/page7/' + str(workReport_id) + '/')
    else:
        data = {
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Направлено в изолятор брака'
         }
    #  c.update(csrf(request))
    return render(request, 'plan/workReportFormset.html', c)

def workReportPage7(request, workReport_id):
    return render(request, 'plan/workReportFinal.html', {'id':workReport_id})

def workersView(request):
    return None


def workerView(request, worker_id):
    return None


def addWorker(request):
    return None


def test(request):
    return render_to_response('plan/test.html', {})


def workReports(request):
    return render_to_response('plan/workReportList.html', {'reports': WorkReport.objects.all()})


def createWorkReport(request):
    w = WorkReport()
    w.save()
    return HttpResponseRedirect('/workReport/page1/' + str(w.pk) + '/')


def printReport(request,workReport_id):
    rationales = [
        ['2,3', 'Я так захотел'],
        ['3,4,5', 'А это заставили']
    ]
    works = [
        ['1', '-', 'Получение наряда и ТМЦ для выполнения работ', '08:30', '08:45'],
        ['2', '1.2.3', 'Изготовление деталей оснастки для сушки лейнеров по прилагаемому чертежу в кол-ве одного '
                       'комплекта', '13:15', '16:15'],
        ['3', '-', 'Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий день,'
                   'проверка инструмента, сдача ТМЦ', '16:15', '16:45'],
        ['4', '1.2.3', 'Уборка рабочего места', '16:45', '17:00'],
    ]

    factWorks = [
        ['1', '-', 'Получение наряда и ТМЦ для выполнения работ', '08:30', '08:45'],
        ['2', '1.2.3', 'Изготовление деталей оснастки для сушки лейнеров по прилагаемому чертежу в кол-ве одного '
                       'комплекта', '13:15', '16:15'],
        ['3', '-', 'Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий'
                   'день, проверка инструмента, сдача ТМЦ ', '16:15', '16:45'],
        ['4', '1.2.3', 'Уборка рабочего места', '16:45', '17:00'],
    ]
    note = '''Примечание 1 (обязательное):
       Максимальный срок проведения ВИК (входного контроля) до конца рабочего дня 16.01.2017 г.'''

    planEquipment = [
        ['Перчатки х/б', '123', 'пара', '1', '0', '0', '0', '-1'],
        ['Пруток бронза', 'Б132r', 'мм', '200', '0', '0', '0', '-1'],
    ]
    nonPlanEquipment = [
        ['asf х/б', '123', 'пара', '1', '0', '0', '0', '-1'],
        ['Пруток бронза', 'Б132r', 'мм', '200', '1', '2', '1', '5'],
    ]
    dust = [
        ['хлам 1', '100'],
        ['хлам 2', '500']
    ]

    document = generateReport('ШАВ', 'Шанин А.В.', 'Бука А.В', '124', "Головнёв А.К.", datetime.date.today(), 'Токарь',
                              rationales, works, factWorks, 'Шанин А.В.', 'Шанин А.В.', 'Хионин Б.Г.', note,
                              'аттестация отутствует', dust, planEquipment, nonPlanEquipment)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=report.docx'
    document.save(response)

    return response

