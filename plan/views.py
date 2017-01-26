# -*- coding: utf-8 -*-
import datetime
import os
from audioop import reverse
from io import StringIO

from django.db import IntegrityError
from django.db import transaction
from django.forms import formset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.contrib import messages
# Create your views here.
from document import Document

from localCode.workReportGenerator import generateReport
from mysite import settings
from plan.forms import ReportForm, LoginForm, WorkPartForm
from plan.models import Worker, WorkReport


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


def workReport(request):
    # если post запрос
    if request.method == 'POST':
        # строим форму на основе запроса
        form = ReportForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            work_report = WorkReport.objects.create(supervisor=form.cleaned_data["supervisor"],
                                                    VIKer=form.cleaned_data["VIKer"],
                                                    reportMaker=form.cleaned_data["reportMaker"],
                                                    reportChecker=form.cleaned_data["reportChecker"],
                                                    worker=form.cleaned_data["worker"],
                                                    stockMan=form.cleaned_data["stockMan"],
                                                    adate=form.cleaned_data["adate"],
                                                    VIKDate=form.cleaned_data["VIKDate"])
            work_report.save()

            # возвращаем простое окно регистрации
            return HttpResponseRedirect(str(work_report.pk) + '/page2/')
        else:
            data = {'supervisor': form.cleaned_data["supervisor"],
                    'VIKer': form.cleaned_data["VIKer"],
                    'reportMaker': form.cleaned_data["reportMaker"],
                    'reportChecker': form.cleaned_data["reportChecker"],
                    'worker': form.cleaned_data["worker"],
                    'stockMan': form.cleaned_data["stockMan"],
                    'date': form.cleaned_data["date"],
                    }
            return render(request, "plan/workReport.html", {
                'form': ReportForm(data),
                'login_form': LoginForm()
            })
    else:
        # возвращаем простое окно регистрации
        return render(request, "plan/workReport.html", {
            'form': ReportForm(),
            'login_form': LoginForm()
        })


def workReportPage2(request, workReport_id):
    wRep = WorkReport.objects.get(pk=workReport_id)

    ArticleFormSet = formset_factory(WorkPartForm)
    if request.method == 'POST':
        formset = ArticleFormSet(request.POST, request.FILES)
        if formset.is_valid():
            print('It works')
            #return HttpResponseRedirect(str(workReport_id) + '/page3/')
    else:
        data = {
        'form-TOTAL_FORMS': u'4',
        'form-INITIAL_FORMS': u'4',
        'form-MAX_NUM_FORMS': u'10',
        }
        formset = ArticleFormSet(data)

    return render_to_response('plan/workReportPage2.html', {'formset': formset})


def workReportPage3(request, workReport_id):
    wRep = WorkReport.objects.get(pk=workReport_id)

    ArticleFormSet = formset_factory(WorkPartForm)
    if request.method == 'POST':
        formset = ArticleFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        data = {
        'form-TOTAL_FORMS': u'4',
        'form-INITIAL_FORMS': u'4',
        'form-MAX_NUM_FORMS': u'10',
        }
        formset = ArticleFormSet(data)

    return render_to_response('plan/workReportPage2.html', {'formset': formset})



def workersView(request):
    return None


def workerView(request, worker_id):
    return None


def addWorker(request):
    return None


