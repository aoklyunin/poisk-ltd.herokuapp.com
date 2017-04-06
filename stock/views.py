# -*- coding: utf-8 -*-
from django.forms.formsets import BaseFormSet, formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from constructors.models import Equipment, StockStruct
from plan.forms import LoginForm
from plan.models import Area
from stock.form import MoveEquipmentForm, EquipmentForm, MoveMaterialForm, MoveDetailForm, MoveAssemblyForm
from stock.models import MoveEquipment
from plan.forms import RequiredFormSet


def extradition(request, area_id):
    EquipmentFormset = formset_factory(MoveEquipmentForm, formset=RequiredFormSet)
    MaterialFormset = formset_factory(MoveMaterialForm, formset=RequiredFormSet)
    DetailFormset = formset_factory(MoveDetailForm, formset=RequiredFormSet)
    AssemblyFormset = formset_factory(MoveAssemblyForm, formset=RequiredFormSet)
    if request.method == 'POST':
        equipment_formset = EquipmentFormset(request.POST, request.FILES, prefix='equipment')
        material_formset = MaterialFormset(request.POST, request.FILES, prefix='material')
        detail_formset = DetailFormset(request.POST, request.FILES, prefix='detail')
        assembly_formset = AssemblyFormset(request.POST, request.FILES, prefix='assembly')
        if equipment_formset.is_valid():
            for form in equipment_formset.forms:
                print(form.cleaned_data)
                eq = form.cleaned_data["equipment"]
                cnt = form.cleaned_data["cnt"]
                e = MoveEquipment.objects.create(
                    equipment=eq,
                    cnt=cnt,
                    flgAcceptance=False,
                )
                e.save()
                e.accept(area_id)

    c = {'equipment_formset': EquipmentFormset(prefix='equipment'),
         'material_formset': MaterialFormset(prefix='detail'),
         'detail_formset': DetailFormset(prefix='detail'),
         'assembly_formset': AssemblyFormset(prefix='assembly'),
         'login_form': LoginForm(),
         'area_id': area_id,
         'one': '1'
         }
    return render(request, 'stock/extradition.html', c)


def acceptance(request, area_id):
    EquipmentFormset = formset_factory(MoveEquipmentForm, formset=RequiredFormSet)
    if request.method == 'POST':
        print(request.POST)
        equipment_formset = EquipmentFormset(request.POST, request.FILES, prefix='equipment')
        if equipment_formset.is_valid():
            for form in equipment_formset.forms:
                eq = form.cleaned_data["equipment"]
                cnt = form.cleaned_data["cnt"]
                e = MoveEquipment.objects.create(
                    equipment=eq,
                    cnt=cnt,
                    flgAcceptance=True,
                )
                e.save()
                e.accept(area_id)

    c = {'equipment_formset': EquipmentFormset(prefix='equipment'),
         'detail_formset': EquipmentFormset(prefix='detail'),
         'assembly_formset': EquipmentFormset(prefix='assembly'),
         'login_form': LoginForm(),
         'area_id': area_id,
         'one': '1'
         }
    return render(request, 'stock/acceptance.html', c)


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
            eq.equipmentType = form.cleaned_data["equipmentType"]
            eq.scheme = form.cleaned_data["scheme"]
            eq.needVIK = form.cleaned_data["needVIK"]
            eq.save()

    return render(request, "stock/detailEquipment.html", {
        'form': EquipmentForm(instance=Equipment.objects.get(pk=equipment_id)),
    })


def removeStockEquipment(request, equipment_id):
    eq = Equipment.objects.get(pk=equipment_id)
    eq.stockStruct.clear()
    eq.delete()

    return HttpResponseRedirect('/stock/equipment/list/0/')


def detailStockMaterial(request, area_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = EquipmentForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            d["dimension"] = form.cleaned_data["dimension"]
            d["equipmentType"] = Equipment.TYPE_EQUIPMENT
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
    for l in Equipment.objects.filter(equipmentType=Equipment.TYPE_EQUIPMENT):
        arr.append({
            "name": l.name,
            "dimension": l.dimension,
            "cnt": l.stockStruct.get(area=area).cnt,
            "id": l.pk
        })

    return render(request, "stock/equipmentList.html", {
        'area_id': area_id,
        'login_form': LoginForm(),
        'eqs': arr,
        'one': '1',
        'form': EquipmentForm(),
    })




def equipmentList(request, area_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = EquipmentForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            d["dimension"] = form.cleaned_data["dimension"]
            d["equipmentType"] = Equipment.TYPE_EQUIPMENT
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
    for l in Equipment.objects.filter(equipmentType=Equipment.TYPE_EQUIPMENT):
        arr.append({
            "name": l.name,
            "dimension": l.dimension,
            "cnt": l.stockStruct.get(area=area).cnt,
            "id": l.pk
        })

    return render(request, "stock/equipmentList.html", {
        'area_id': area_id,
        'login_form': LoginForm(),
        'eqs': arr,
        'one': '1',
        'form': EquipmentForm(),
    })


def workReportList(request):
    print("sadas")
    return render(request, "stock/workReportList9.html", {
    })
