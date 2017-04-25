# -*- coding: utf-8 -*-
from django.forms import TextInput
from django.forms.formsets import BaseFormSet, formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from constructors.models import Equipment, StockStruct
from plan.forms import LoginForm
from plan.models import Area
from stock.form import MoveEquipmentForm, EquipmentForm, MoveMaterialForm, MoveDetailForm, MoveAssemblyForm
from stock.models import MoveEquipment
from plan.forms import RequiredFormSet


# список оборудования по типу оборудования
def listEquipmentByType(request, area_id, tp, template):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = EquipmentForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            d["dimension"] = form.cleaned_data["dimension"]
            d["equipmentType"] = tp
            eq = Equipment.objects.create()
            ms = StockStruct.objects.create(area=Area.objects.get(name="Малахит"))
            ks = StockStruct.objects.create(area=Area.objects.get(name="Красное село"))
            eq.stockStruct.add(ms)
            eq.stockStruct.add(ks)
            eq.save()
            Equipment.objects.filter(pk=eq.pk).update(**d)

    if int(area_id) == 0:
        area = Area.objects.get(name="Красное село")
    else:
        area = Area.objects.get(name="Малахит")

    arr = []
    for l in Equipment.objects.filter(equipmentType=tp):
        arr.append({
            "name": l.name,
            "dimension": l.dimension,
            "cnt": 0 if l.equipmentType == Equipment.TYPE_STANDART_WORK else l.stockStruct.get(area=area).cnt,
            "id": l.pk
        })
    ef = EquipmentForm()

    ef.fields["name"].label = ""

    if tp == Equipment.TYPE_STANDART_WORK:
        ef.fields["name"].widget = TextInput(attrs={'placeholder': 'Сварка'})
    elif tp == Equipment.TYPE_DETAIL:
        ef.fields["name"].widget = TextInput(attrs={'placeholder': 'Деталь 1'})
    elif tp == Equipment.TYPE_ASSEMBLY_UNIT:
        ef.fields["name"].widget = TextInput(attrs={'placeholder': 'Сборка 1'})

    return render(request, template, {
        'area_id': area_id,
        'login_form': LoginForm(),
        'eqs': arr,
        'one': '1',
        'form': ef,
    })


# список оснастки
def equipmentList(request, area_id):
    return listEquipmentByType(request, area_id, Equipment.TYPE_EQUIPMENT, "stock/equipmentList.html")


# список материалов
def materialList(request, area_id):
    return listEquipmentByType(request, area_id, Equipment.TYPE_MATERIAL, "stock/materialList.html")


# список деталей
def detailList(request, area_id):
    return listEquipmentByType(request, area_id, Equipment.TYPE_DETAIL, "stock/detailList.html")


# список Сборочных единиц
def assemblyList(request, area_id):
    return listEquipmentByType(request, area_id, Equipment.TYPE_ASSEMBLY_UNIT, "stock/assemblyList.html")


# детализация по оборудованию на складе
def detailStockEquipment(request, equipment_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = EquipmentForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            eq = Equipment.objects.get(pk=equipment_id)
            eq.name = form.cleaned_data["name"]
            eq.dimension = form.cleaned_data["dimension"]
            eq.code = form.cleaned_data["code"]
            eq.scheme = form.cleaned_data["scheme"]
            eq.needVIK = form.cleaned_data["needVIK"]
            eq.save()
            if eq.equipmentType == Equipment.TYPE_EQUIPMENT:
                return HttpResponseRedirect('/stock/equipment/list/0/')
            else:
                return HttpResponseRedirect('/stock/material/list/0/')

    return render(request, "stock/detailEquipment.html", {
        'form': EquipmentForm(instance=Equipment.objects.get(pk=equipment_id)),
    })


# обработать формсет движения оборудования(приёмка/выдача)
def processMovingFomset(formset, flgAcceptance, area_id):
    if formset.is_valid():
        for form in formset.forms:
            if ("equipment" in form.cleaned_data.keys()) and ("cnt" in form.cleaned_data.keys()):
                print(form.cleaned_data)
                eq = form.cleaned_data["equipment"]
                cnt = form.cleaned_data["cnt"]
                if (cnt is not None):
                    e = MoveEquipment.objects.create(
                        equipment=eq,
                        cnt=cnt,
                        flgAcceptance=flgAcceptance,
                    )
                    e.save()
                    e.accept(area_id)


def moving(request, area_id, flgAcceptance, template):
    EquipmentFormset = formset_factory(MoveEquipmentForm, formset=RequiredFormSet)
    MaterialFormset = formset_factory(MoveMaterialForm, formset=RequiredFormSet)
    DetailFormset = formset_factory(MoveDetailForm, formset=RequiredFormSet)
    AssemblyFormset = formset_factory(MoveAssemblyForm, formset=RequiredFormSet)
    if request.method == 'POST':
        processMovingFomset(EquipmentFormset(request.POST, request.FILES, prefix='equipment'), flgAcceptance, area_id)
        processMovingFomset(MaterialFormset(request.POST, request.FILES, prefix='material'), flgAcceptance, area_id)
        processMovingFomset(DetailFormset(request.POST, request.FILES, prefix='detail'), flgAcceptance, area_id)
        processMovingFomset(AssemblyFormset(request.POST, request.FILES, prefix='assembly'), flgAcceptance, area_id)

    c = {'equipment_formset': EquipmentFormset(prefix='equipment'),
         'material_formset': MaterialFormset(prefix='material'),
         'detail_formset': DetailFormset(prefix='detail'),
         'assembly_formset': AssemblyFormset(prefix='assembly'),
         'login_form': LoginForm(),
         'area_id': area_id,
         'one': '1'
         }
    return render(request, template, c)


# выдача
def extradition(request, area_id):
    return moving(request, area_id, False, 'stock/extradition.html')


# приёмка
def acceptance(request, area_id):
    return moving(request, area_id, True, 'stock/acceptance.html')


# удаление оборудования
def removeStockEquipment(request, equipment_id):
    eq = Equipment.objects.get(pk=equipment_id)
    tp = eq.equipmentType
    eq.stockStruct.clear()
    eq.delete()

    if tp == Equipment.TYPE_EQUIPMENT:
        return HttpResponseRedirect('/stock/equipment/list/0/')
    else:
        return HttpResponseRedirect('/stock/material/list/0/')


# список нарядов
def reportList(request, area_id):
    return render(request, "stock/reportList.html", {
        'login_form': LoginForm(),
        'area_id': area_id,

        'one': '1'
    })
