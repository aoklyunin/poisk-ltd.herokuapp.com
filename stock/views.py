# -*- coding: utf-8 -*-
from django.contrib import messages
from django.forms import TextInput
from django.forms.formsets import BaseFormSet, formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from constructors.form import EquipmentListWithoutSWForm, EquipmentListForm, EquipmentCntWithoutSWForm, \
    EquipmentSingleWithCtnForm, EquipmentConstructorForm, EquipmentConstructorSingleForm, AddEquipmentForm
from constructors.models import Equipment, StockStruct
from plan.forms import LoginForm, subdict
from plan.models import Area, InfoText
from stock.form import StockReadyReportSingleForm, StockLeaveReportSingleForm, StockLeaveReportForm, \
    StockEquipmentListForm, StockEquipmentCntForm, ProviderSingleForm, AddProviderForm, ProviderForm
from stock.models import MoveEquipment, Provider
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


def stockListAll(request, area_id):
    lst = []
    area = Area.objects.get(pk=area_id)
    for eq in Equipment.objects.all().exclude(equipmentType=Equipment.TYPE_STANDART_WORK):
        flg = True
        for ss in eq.stockStruct.all():
            if ss.area == area:
                lst.append([eq, ss.cnt])
                flg = False
        if flg:
            messages.error(request, "На этой площадке не найдено складской структуры " + eq.name)
    # формируем страницу со списком
    c = {
        'area_id': int(area_id),  # иначе не сравнить с id площадки при переборе
        'login_form': LoginForm(),
        'lst': lst,
        'areas': Area.objects.all().order_by('name'),
    }
    return render(request, "stock/stockList.html", c)


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
            wr.processAcceptanceFormset(equipment_formset, wr.area)
            return HttpResponseRedirect("/stock/wrAcceptance/" + str(wr.area) + "/")

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


# обработать формсет движения оборудования(приёмка/выдача)
def processMovingFomset(formset, flgAcceptance, area_id):
    if formset.is_valid():
        for form in formset.forms:
            try:
                if ("equipment" in form.cleaned_data.keys()) and ("cnt" in form.cleaned_data.keys()):
                    eq = Equipment.objects.get(pk=int(form.cleaned_data["equipment"]))
                    cnt = form.cleaned_data["cnt"]
                    if (cnt is not None):
                        e = MoveEquipment.objects.create(
                            equipment=eq,
                            cnt=cnt,
                            flgAcceptance=flgAcceptance,
                        )
                        e.save()
                        e.acceptMoving(area_id)
            except:
                print("acceptance: ошибка чтения формы")


# приём поставки
def acceptance(request, area_id):
    EquipmentFormset = formset_factory(EquipmentCntWithoutSWForm)
    if request.method == 'POST':
        report_formset = EquipmentFormset(request.POST, request.FILES, prefix="equipment")
        if report_formset.is_valid():
            processMovingFomset(report_formset, True, area_id)

    c = {
        'login_form': LoginForm(),
        'area_id': int(area_id),
        'link_formset': EquipmentFormset(prefix='equipment')
    }
    return render(request, "stock/acceptance.html", c)


# список поставщиков
def providers(request):
    if request.method == "POST":
        # форма редактирования оборудования
        eq_form = ProviderSingleForm(request.POST, prefix='eq_form')
        # если форма заполнена корректно
        if eq_form.is_valid():
            pr = Provider.objects.get(pk=int(eq_form.cleaned_data['provider']))
            return HttpResponseRedirect('/stock/detailProvider/' + str(pr.pk) + '/')
    c = {
        'login_form': LoginForm(),
        'eq_form': ProviderSingleForm(prefix="eq_form"),
        'form': AddProviderForm(prefix="main_form"),
        'area_id': Area.objects.first().pk,
    }
    return render(request, "stock/providers.html", c)

# создать поставщика
def createProvider(request):
    if request.method == "POST":
        # форма редактирования оборудования
        eq_form = AddProviderForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if eq_form.is_valid():
            pr = Provider.objects.create(name = eq_form.cleaned_data['name'])
            return HttpResponseRedirect('/stock/detailProvider/' + str(pr.pk) + '/')

    return HttpResponseRedirect('/stock/providers/')


# детализация поставщика
def detailProvider(request, provider_id):
    provider = Provider.objects.get(pk = provider_id)
    if request.method == 'POST':
        provider_form = ProviderForm(request.POST, request.FILES, prefix='equipment')
        if provider_form.is_valid():
            Provider.objects.filter(pk=provider_id).update(**provider_form.cleaned_data)


    c = {'form': ProviderForm(instance=provider, prefix='equipment'),
         'login_form': LoginForm(),
         'provider_id': provider_id,
         'area_id': Area.objects.first().pk,
         }
    return render(request, "stock/detailProvider.html", c)


def deleteProvider(request, provider_id):
    Provider.objects.filter(pk=provider_id).delete()
    return HttpResponseRedirect('/stock/providers/')



# список поставщиков
def equipment(request):
    if request.method == "POST":
        # форма редактирования оборудования
        eq_form = ProviderSingleForm(request.POST, prefix='eq_form')
        # если форма заполнена корректно
        if eq_form.is_valid():
            pr = Provider.objects.get(pk=int(eq_form.cleaned_data['provider']))
            return HttpResponseRedirect('/stock/detailProvider/' + str(pr.pk) + '/')
    c = {
        'login_form': LoginForm(),
        'eq_form': ProviderSingleForm(prefix="eq_form"),
        'form': AddProviderForm(prefix="main_form"),
        'area_id': Area.objects.first().pk,
    }
    return render(request, "stock/equipment.html", c)

# создать поставщика
def createEquipment(request):
    if request.method == "POST":
        # форма редактирования оборудования
        eq_form = AddProviderForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if eq_form.is_valid():
            pr = Provider.objects.create(name = eq_form.cleaned_data['name'])
            return HttpResponseRedirect('/stock/detailProvider/' + str(pr.pk) + '/')

    return HttpResponseRedirect('/stock/providers/')


# детализация поставщика
def detailEquipment(request, provider_id):
    provider = Provider.objects.get(pk = provider_id)
    if request.method == 'POST':
        provider_form = ProviderForm(request.POST, request.FILES, prefix='equipment')
        if provider_form.is_valid():
            Provider.objects.filter(pk=provider_id).update(**provider_form.cleaned_data)


    c = {'form': ProviderForm(instance=provider, prefix='equipment'),
         'login_form': LoginForm(),
         'provider_id': provider_id,
         'area_id': Area.objects.first().pk,
         }
    return render(request, "stock/detailProvider.html", c)



def deleteEquipment(request, provider_id):
    Provider.objects.filter(pk=provider_id).delete()
    return HttpResponseRedirect('/stock/providers/')
