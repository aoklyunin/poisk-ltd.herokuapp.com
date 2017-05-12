# -*- coding: utf-8 -*-
from django.contrib import messages
from django.forms import TextInput
from django.forms.formsets import BaseFormSet, formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from constructors.form import EquipmentListWithoutSWForm, EquipmentListForm
from constructors.models import Equipment, StockStruct
from plan.forms import LoginForm
from plan.models import Area, InfoText
from stock.form import MoveEquipmentForm, MoveMaterialForm, MoveDetailForm, MoveAssemblyForm, EquipmentForm, \
    StockReadyReportSingleForm, StockLeaveReportSingleForm, StockLeaveReportForm
from stock.models import MoveEquipment
from plan.forms import RequiredFormSet

# главная страница раздела нарядов
from workReport.models import WorkReport


def index(request):
    c = {
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="stock_index"),
        'area_id': Area.objects.first().pk,
    }
    return render(request, "stock/index.html", c)


# баланс на складе
def stockBalance(request, area_id):
    if request.method == "POST":
        # строим форму на основе запроса
        form = EquipmentListForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            # получаем объект площадки
            area = Area.objects.get(pk=area_id)
            # формируем список оборудования, у которого есть данные об этой площадке
            lst = []
            for e in form.cleaned_data['equipment']:
                try:
                    eq = Equipment.objects.get(pk=e)
                    flg = True
                    for ss in eq.stockStruct.all():
                        if ss.area == area:
                            lst.append([eq, ss.cnt])
                            flg = False
                    if flg:
                        messages.error(request, "На этой площадке не найдено складской структуры " + eq.name)
                except:
                    messages.error(request, "Оборудования с таким id не найдено")
            # если списокнепустой
            if len(lst) > 0:
                # формируем страницу со списком
                c = {
                    'area_id': int(area_id),  # иначе не сравнить с id площадки при переборе
                    'login_form': LoginForm(),
                    'lst': lst,
                    'areas': Area.objects.all().order_by('name'),
                }
                return render(request, "stock/stockList.html", c)

    c = {
        'area_id': int(area_id),  # иначе не сравнить с id площадки при переборе
        'areas': Area.objects.all().order_by('name'),
        'login_form': LoginForm(),
        'form': EquipmentListWithoutSWForm(prefix="main_form")
    }
    return render(request, "stock/stockBalance.html", c)


# Выдача нарядов
def wrExtradition(request, area_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = StockReadyReportSingleForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            return HttpResponseRedirect("/stock/detailWrExtradition/" + form.cleaned_data["report"] + "/")

    c = {
        'login_form': LoginForm(),
        'area_id': int(area_id),
        'areas': Area.objects.all().order_by('name'),
        'reportForm': StockReadyReportSingleForm(),
    }
    return render(request, "stock/wrExtradition.html", c)


# выдача по конкретному наряду
def detailWrExtradition(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)

    if request.method == 'POST':
        # строим форму на основе запроса
        form = StockReadyReportSingleForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            return HttpResponseRedirect("/stock/wrExtradition/" + form.cleaned_data["report"] + "/")

    pE = wr.generateHardwareVals()

    c = {
        'pE': pE,
        'login_form': LoginForm(),
        'area_id': Area.objects.first().pk,
        'areas': Area.objects.all().order_by('name'),
        'reportForm': StockReadyReportSingleForm(),
        'wr': wr,
    }
    return render(request, "stock/detailWrExtradition.html", c)


def doWrExtradition(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    wr.extraditionEquipment()

    return HttpResponseRedirect("/stock/wrExtradition/" + str(Area.objects.first().pk) + "/")


# главная страница раздела нарядов
def wrAcceptance(request, area_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = StockLeaveReportSingleForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            return HttpResponseRedirect("/stock/detailWrAcceptance/" + form.cleaned_data["report"] + "/")

    c = {
        'login_form': LoginForm(),
        'area_id': int(area_id),
        'areas': Area.objects.all().order_by('name'),
        'reportForm': StockLeaveReportSingleForm(),
    }
    return render(request, "stock/wrAcceptance.html", c)


# выдача по конкретному наряду
def detailWrAcceptance(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    EquipmentFormset = formset_factory(StockLeaveReportForm)
    if request.method == 'POST':
        equipment_formset = EquipmentFormset(request.POST, request.FILES, prefix='equipment')
        if equipment_formset.is_valid():
            wr.processAcceptanceFormset(equipment_formset)
            return HttpResponseRedirect("/stock/wrAcceptance/"+str(wr.area)+"/")

    data = wr.generateAcceptanceData()
    c = {
        'link_formset': EquipmentFormset(initial=data, prefix='equipment'),
        'formset_length': len(data),
        'login_form': LoginForm(),
        'area_id': Area.objects.first().pk,
        'areas': Area.objects.all().order_by('name'),
        'wr': wr,
    }
    return render(request, "stock/detailWrAcceptance.html", c)


# главная страница раздела нарядов
def acceptance(request, area_id):
    c = {
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="stock_index"),
        'area_id': Area.objects.first().pk,
    }
    return render(request, "stock/index.html", c)


# главная страница раздела нарядов
def providers(request):
    c = {
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="stock_index"),
        'area_id': Area.objects.first().pk,
    }
    return render(request, "stock/index.html", c)


# главная страница раздела нарядов
def equipment(request, area_id):
    c = {
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="stock_index"),
        'area_id': Area.objects.first().pk,
    }
    return render(request, "stock/equipment.html", c)
