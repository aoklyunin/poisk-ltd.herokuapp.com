# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from plan.forms import LoginForm
from plan.models import Area
from stock.form import EquipmentForm
from workReport.models import StockStruct, Equipment


def workReportList(request):
    return render(request, "constructors/workReportList.html", {

    })


def removeEquipment(request, equipment_id):
    eq = Equipment.objects.get(pk=equipment_id)
    eq.stockStruct.clear()
    eq.delete()

    return HttpResponseRedirect('/stock/equipment/list/0/')


def detailEquipment(request, equipment_id):
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
        return HttpResponseRedirect('/constructors/list/'+str(eq.equipmentType)+'/0/')

    return render(request, "constructors/detailEquipment.html", {
        'form': EquipmentForm(instance=Equipment.objects.get(pk=equipment_id)),
    })


def detailStandartWork(request, swork_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = EquipmentForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            eq = Equipment.objects.get(pk=swork_id)
            eq.name = form.cleaned_data["name"]
            eq.dimension = form.cleaned_data["dimension"]
            eq.code = form.cleaned_data["code"]
            eq.equipmentType = form.cleaned_data["equipmentType"]
            eq.scheme = form.cleaned_data["scheme"]
            eq.needVIK = form.cleaned_data["needVIK"]
            eq.save()

    return render(request, "stock/detailEquipment.html", {
        'form': EquipmentForm(instance=Equipment.objects.get(pk=swork_id)),
    })


def listEquipment(request, equipment_type, area_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = EquipmentForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            d["dimension"] = form.cleaned_data["dimension"]
            d["equipmentType"] = equipment_type
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
    for l in Equipment.objects.filter(equipmentType=equipment_type):
        arr.append({
            "name": l.name,
            "dimension": l.dimension,
            "cnt": l.stockStruct.get(area=area).cnt,
            "id": l.pk
        })
    print(arr)

    return render(request, "constructors/equipmentList.html", {
        'area_id': area_id,
        'equipment_type': equipment_type,
        'login_form': LoginForm(),
        'eqs': arr,
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'form': EquipmentForm(),
    })


def listStandartWork(request):
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

    return render(request, "constructors/standartWorkList.html", {
        'login_form': LoginForm(),
        'one': '1',
        'form': EquipmentForm(),
    })
