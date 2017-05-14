# -*- coding: utf-8 -*-
from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from constructors.form import SchemeForm, EquipmentListForm, EquipmentConstructorSingleForm, AddEquipmentForm, \
    EquipmentSingleWithCtnForm, SchemeSingleForm, EquipmentListWithoutSWForm, EquipmentConstructorForm
from plan.forms import LoginForm, subdict
from plan.models import Area, Scheme, InfoText
from .models import StockStruct, Equipment


# главная страница конструкторского отдела
def index(request):
    c = {
        'area_id': Area.objects.first().pk,
        'login_form': LoginForm(),
        'it': InfoText.objects.get(pageName="constructor_index"),
        'pageTitleHeader': 'Конструкторам',
    }
    return render(request, "constructors/index.html", c)


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
                    'login_form': LoginForm(),
                    'lst': lst,
                    'area_id': int(area_id),
                    'pageTitle': 'Конструкторам',
                    'pageHeader': 'Конструкторам',
                }
                return render(request, "constructors/stockList.html", c)

    c = {
        'area_id': int(area_id),  # иначе не сравнить с id площадки при переборе
        'areas': Area.objects.all().order_by('name'),
        'curPageLink': "/constructors/stock_balance/",
        'login_form': LoginForm(),
        'chooseForm': EquipmentListWithoutSWForm(prefix="main_form"),
        'pageTitleHeader': 'Конструкторам',
        'chooseHeader': 'Выберите оборудование, баланс которого на сладе надо отобразить',
        'chooseHints': [{"id": "equipment", "text": "Выберите оборудование"}]
    }
    return render(request, "constructors/stockBalance.html", c)


# страница конструкторской работы
def tehnology(request):
    if request.method == "POST":
        # форма редактирования оборудования
        eq_form = EquipmentConstructorSingleForm(request.POST, prefix='eq_form')
        # если форма заполнена корректно
        if eq_form.is_valid():
            print(eq_form.cleaned_data)
            eq = Equipment.objects.get(pk=int(eq_form.cleaned_data['equipment']))
            return HttpResponseRedirect('/constructors/detail/' + str(eq.pk) + '/')
    c = {
        'login_form': LoginForm(),
        'eq_form': EquipmentConstructorSingleForm(prefix="eq_form"),
        'form': AddEquipmentForm(prefix="main_form"),
        'area_id': Area.objects.first().pk,
        'pageTitleHeader': 'Конструкторам',
        'chooseHeader': 'Выберите оборудование, которое Вы хотите поменять',
        'chooseHints': [{"id": "equipment", "text": "Выберите оборудование"}]
    }
    return render(request, "constructors/tehnology.html", c)


# добавление оборудования
def addEquipment(request):
    if request.method == "POST":
        # форма добавления оборужования
        form = AddEquipmentForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            d["equipmentType"] = form.cleaned_data["tp"]
            eq = Equipment.objects.create()
            if d["equipmentType"] == Equipment.TYPE_STANDART_WORK:
                d["dimension"] = "час"
            else:
                d["dimension"] = "шт."
            for area in Area.objects.all():
                s = StockStruct.objects.create(area=area)
                eq.stockStruct.add(s)
            eq.save()
            Equipment.objects.filter(pk=eq.pk).update(**d)
            return HttpResponseRedirect('/constructors/detail/' + str(eq.pk) + '/')
    return HttpResponseRedirect('/constructors/work/')


# детализация оборужования
def detailEquipment(request, eq_id):
    EquipmentFormset = formset_factory(EquipmentSingleWithCtnForm)

    eq = Equipment.objects.get(pk=eq_id)

    if request.method == 'POST':
        # строим форму на основе запроса
        form = EquipmentConstructorForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = subdict(form, ("name", "needVIK", "equipmentType"))
            Equipment.objects.filter(pk=eq_id).update(**d)
            eq = Equipment.objects.get(pk=eq_id)
            if eq.equipmentType == Equipment.TYPE_STANDART_WORK:
                try:
                    eq.duration = form.cleaned_data["duration"]
                except:
                    messages.error("Не получилось задать длительность работы")
            else:
                try:
                    eq.code = form.cleaned_data["code"]
                except:
                    messages.error("Не получилось задать шифр изделия")
            eq.scheme.clear()
            for e in form.cleaned_data["scheme"]:
                eq.scheme.add(e)
            eq.save()
        equipment_formset = EquipmentFormset(request.POST, request.FILES, prefix='equipment')
        eq.addFromFormset(equipment_formset, True)
        gen_formset = EquipmentFormset(request.POST, request.FILES, prefix='gen')
        eq.addGenEquipmentFromFormset(gen_formset, True)

    ef = EquipmentConstructorForm(instance=Equipment.objects.get(pk=eq_id), initial={'scheme': eq.getSchemeChoices()},
                                  prefix="main_form")
    ef.fields["equipmentType"].initial = eq.equipmentType

    #  print(eq.generateDataFromNeedStructs())
    #  print( EquipmentFormset(initial=eq.generateDataFromNeedStructs(), prefix='equipment'))
    c = {'equipment_formset': EquipmentFormset(initial=eq.generateDataFromNeedStructs(), prefix='equipment'),
         'gen_formset': EquipmentFormset(initial=eq.generateDataFromGenEquipment(), prefix='gen'),
         'login_form': LoginForm(),
         'one': '1',
         'form': ef,
         'eqType': eq.equipmentType,
         'tsw': Equipment.TYPE_STANDART_WORK,
         'eq_id': eq_id,
         'area_id': Area.objects.first().pk,
         }
    return render(request, "constructors/detail.html", c)


# удалить конструкторское оборудование
def deleteConstructorEquipment(request, eq_id):
    eq = Equipment.objects.get(pk=eq_id)
    eq.stockStruct.clear()
    eq.delete()
    return HttpResponseRedirect('/constructors/tehnology/')


# список чертежей
def shemes(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = SchemeSingleForm(request.POST, prefix="single-scheme")
        # если форма заполнена корректно
        if form.is_valid():
            return HttpResponseRedirect('/constructors/sheme/detail/' + str(form.cleaned_data["scheme"]) + '/')

    return render(request, "constructors/shemesList.html", {
        'login_form': LoginForm(),
        'schs': Scheme.objects.all(),
        'one': '1',
        'addForm': SchemeForm(prefix="add-scheme"),
        'singleForm': SchemeSingleForm(prefix="single-scheme"),
        'area_id': Area.objects.first().pk,
    })


# Добавить чертеж
def addScheme(request):
    if request.method == "POST":
        # форма добавления оборужования
        form = SchemeForm(request.POST, prefix='add-scheme')
        # если форма заполнена корректно
        if form.is_valid():
            code = form.cleaned_data["code"]
            sch = Scheme.objects.create(link=form.cleaned_data["link"], author=form.cleaned_data["author"])
            sch.save()
            if (code is not None):
                sch.code = code
                sch.save()
            return HttpResponseRedirect('/constructors/sheme/detail/' + str(sch.pk) + '/')
    return HttpResponseRedirect('/constructors/work/')


# Детализация чертежа
def shemeDetail(request, sh_id):
    if request.method == "POST":
        # форма добавления оборужования
        form = SchemeForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            sch = Scheme.objects.get(pk=sh_id)
            code = form.cleaned_data["code"]
            sch.link = form.cleaned_data["link"]
            sch.author = form.cleaned_data["author"]
            if (code is not None):
                sch.code = code
            sch.save()

    return render(request, "constructors/shemesDetail.html", {
        'login_form': LoginForm(),
        'form': SchemeForm(instance=Scheme.objects.get(pk=sh_id)),
        'area_id': Area.objects.first().pk,
    })
