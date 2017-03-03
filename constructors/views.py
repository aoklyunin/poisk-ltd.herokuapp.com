# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from plan.forms import LoginForm
from plan.models import Area
from workReport.models import StockStruct


def workReportList(request):
    return render(request, "constructors/workReportList.html", {

    })

def addDetail(request):
    return render(request, "constructors/add.html", {

    })

def addAssembly(request):
    return render(request, "constructors/workReportList.html", {

    })

def addStandartWork(request):
    return render(request, "constructors/workReportList.html", {

    })

def detailDetail(request,assembly_id):
    return render(request, "constructors/detail.html", {

    })

def detailAssembly(request,assembly_id):
    return render(request, "constructors/workReportList.html", {

    })

def detailStandartWork(request,assembly_id):
    return render(request, "constructors/workReportList.html", {

    })



def listStandartWork(request, area_id):
    return render(request, "constructors/workReportList.html", {

    })

def listAssembly(request, area_id):
    return render(request, "constructors/workReportList.html", {

    })

def listDetail(request, area_id):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = DetailForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            d = {}
            d["name"] = form.cleaned_data["name"]
            d["dimension"] = form.cleaned_data["dimension"]
            eq = Detail.objects.create()
            ms = StockStruct.objects.create(area=Area.objects.get(name="Малахит"))
            ks = StockStruct.objects.create(area=Area.objects.get(name="Красное село"))
            eq.stockStruct.add(ms)
            eq.stockStruct.add(ks)
            eq.save()
            Detail.objects.filter(pk=eq.pk).update(**d)

    if int(area_id) == 0:
        area = Area.objects.get(name="Красное село")
    else:
        area = Area.objects.get(name="Малахит")

    arr = []
    for l in Detail.objects.all():
        arr.append({
            "name": l.name,
            "cnt": l.stockStruct.get(area=area).cnt,
            "id": l.pk
        })

    return render(request, "stock/equipmentList.html", {
        'area_id': area_id,
        'login_form': LoginForm(),
        'eqs': arr,
        'one': '1',
        'form': DetailForm(),
    })
