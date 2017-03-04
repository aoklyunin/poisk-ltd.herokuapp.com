# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from plan.forms import LoginForm, subdict
from plan.models import Area, WorkerPosition
from stock.form import EquipmentForm, StandartWorkForm
from workReport.models import StockStruct, Equipment, StandartWork


def workReportList(request):
    return render(request, "constructors/workReportList.html", {

    })


def removeEquipment(request, equipment_id):
    eq = Equipment.objects.get(pk=equipment_id)
    eq.stockStruct.clear()
    eq.delete()

    return HttpResponseRedirect('/constructors/equipment/list/0/0/' + str(eq.equipmentType) + '/')


def removeStandartWork(request, swork_id):
    eq = StandartWork.objects.get(pk=swork_id)
    eq.delete()
    return HttpResponseRedirect('/constructors/standartWork/list/')


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
        return HttpResponseRedirect('/constructors/list/equipment/' + str(eq.equipmentType) + '/0/')

    return render(request, "constructors/detailEquipment.html", {
        'form': EquipmentForm(instance=Equipment.objects.get(pk=equipment_id)),
    })


def detailStandartWork(request, swork_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = StandartWorkForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = subdict(form, ("text", "needVIK"))
            StandartWork.objects.filter(pk=swork_id).update(**d)
            StandartWork.objects.get(pk=swork_id).positionsEnable.clear()
            for e in form.cleaned_data["positionsEnable"]:
                StandartWork.objects.get(pk=swork_id).positionsEnable.add(
                    WorkerPosition.objects.get(name=e)
                )
            return HttpResponseRedirect('/constructors/list/standartWork/')
    return render(request, "constructors/detailStandartWork.html", {
        'form': StandartWorkForm(instance=StandartWork.objects.get(pk=swork_id)),
    })


def listEquipment(request, equipment_type, area_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = EquipmentForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            if int(equipment_type) > 1:
                d["dimension"] = 'шт.'
            else:
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
        form = StandartWorkForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["text"] = form.cleaned_data["text"]
            eq = StandartWork.objects.create()
            eq.save()
            StandartWork.objects.filter(pk=eq.pk).update(**d)

    return render(request, "constructors/standartWorkList.html", {
        'login_form': LoginForm(),
        'eqs': StandartWork.objects.all(),
        'one': '1',
        'form': StandartWorkForm(),
    })
