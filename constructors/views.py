# -*- coding: utf-8 -*-
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from constructors.form import SchemeForm
from plan.forms import LoginForm, subdict
from plan.models import Area, WorkerPosition, Scheme
from stock.form import EquipmentForm, StandartWorkForm, MoveEquipmentForm, MoveMaterialForm, MoveDetailForm, \
    MoveAssemblyForm, MoveStandartWorkForm
from stock.views import listEquipmentByType
from .models import StockStruct, Equipment, StandartWork


# список оснастки
def equipmentList(request, area_id):
    return listEquipmentByType(request, area_id, Equipment.TYPE_EQUIPMENT, "constructors/equipmentList.html")


# список материалов
def materialList(request, area_id):
    return listEquipmentByType(request, area_id, Equipment.TYPE_MATERIAL, "constructors/materialList.html")


# список деталей
def detailList(request, area_id):
    return listEquipmentByType(request, area_id, Equipment.TYPE_DETAIL, "constructors/detailList.html")

# список Сборочных единиц
def assemblyList(request, area_id):
    return listEquipmentByType(request, area_id, Equipment.TYPE_ASSEMBLY_UNIT, "constructors/assemblyList.html")

# список стандартных единиц
def standartWorkList(request):
    return listEquipmentByType(request,0, Equipment.TYPE_STANDART_WORK, "constructors/standartWorkList.html")

# удалить конструкторское оборудование
def removeConstructorEquipment(request, equipment_id):
    eq = Equipment.objects.get(pk=equipment_id)
    eq.stockStruct.clear()
    eq.delete()
    return HttpResponseRedirect('/constructors/detail/list/0/')

# редактировать оборудование
def detailConstructorEquipment(request, equipment_id):
    EquipmentFormset = formset_factory(MoveEquipmentForm)
    MaterialFormset = formset_factory(MoveMaterialForm)
    DetailFormset = formset_factory(MoveDetailForm)
    AssemblyFormset = formset_factory(MoveAssemblyForm)
    StandartWorkFormset = formset_factory(MoveStandartWorkForm)

    eq = Equipment.objects.get(pk=equipment_id)

    if request.method == 'POST':
        equipment_formset = EquipmentFormset(request.POST, request.FILES, prefix='equipment')
        material_formset = MaterialFormset(request.POST, request.FILES, prefix='material')
        detail_formset = DetailFormset(request.POST, request.FILES, prefix='detail')
        assembly_formset = AssemblyFormset(request.POST, request.FILES, prefix='assembly')
        swork_formset = StandartWorkFormset(request.POST, request.FILES, prefix='standart_work')

        eq.addFromFormset(equipment_formset, True)
        eq.addFromFormset(material_formset)
        eq.addFromFormset(detail_formset)
        eq.addFromFormset(assembly_formset)
        eq.addFromFormset(swork_formset)

        # строим форму на основе запроса
        form = EquipmentForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = subdict(form, ("name", "dimension", "code", "needVIK"))
            Equipment.objects.filter(pk=equipment_id).update(**d)
            Equipment.objects.get(pk=equipment_id).scheme.clear()
            for e in form.cleaned_data["scheme"]:
                Equipment.objects.get(pk=equipment_id).scheme.add(
                    Scheme.objects.get(name=e)
                )
        return HttpResponseRedirect('/constructors/list/equipment/' + str(eq.equipmentType) + '/0/')

    c = {'equipment_formset': EquipmentFormset(initial=eq.generateDataFromNeedStructs(
        NeedEquipmentType=Equipment.TYPE_EQUIPMENT), prefix='equipment', ),
        'material_formset': MaterialFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_MATERIAL), prefix='material'),
        'detail_formset': DetailFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_DETAIL), prefix='detail', ),
        'assembly_formset': AssemblyFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_ASSEMBLY_UNIT), prefix='assembly', ),
        'swork_formset': StandartWorkFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_STANDART_WORK), prefix='standart_work', ),
        'login_form': LoginForm(),
        'one': '1',
        'form': EquipmentForm(instance=Equipment.objects.get(pk=equipment_id), prefix="main_form"),
        'eqType': eq.equipmentType,
    }

    return render(request, "constructors/detail.html", c)




def removeStandartWork(request, swork_id):
    eq = StandartWork.objects.get(pk=swork_id)
    eq.delete()
    return HttpResponseRedirect('/constructors/standartWork/list/')





def detailStandartWork(request, swork_id):
    EquipmentFormset = formset_factory(MoveEquipmentForm)
    MaterialFormset = formset_factory(MoveMaterialForm)
    DetailFormset = formset_factory(MoveDetailForm)
    AssemblyFormset = formset_factory(MoveAssemblyForm)
    StandartWorkFormset = formset_factory(MoveStandartWorkForm)

    eq = StandartWork.objects.get(pk=swork_id)

    if request.method == 'POST':
        equipment_formset = EquipmentFormset(request.POST, request.FILES, prefix='equipment')
        material_formset = MaterialFormset(request.POST, request.FILES, prefix='material')
        detail_formset = DetailFormset(request.POST, request.FILES, prefix='detail')
        assembly_formset = AssemblyFormset(request.POST, request.FILES, prefix='assembly')
        swork_formset = StandartWorkFormset(request.POST, request.FILES, prefix='standart_work')

        print(equipment_formset)
        print(material_formset)
        print(detail_formset)
        eq.addFromFormset(equipment_formset, True)
        eq.addFromFormset(material_formset)
        eq.addFromFormset(detail_formset)
        eq.addFromFormset(assembly_formset)
        eq.addFromFormset(swork_formset)

        # строим форму на основе запроса
        form = StandartWorkForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            d = subdict(form, ("text", "duration"))
            StandartWork.objects.filter(pk=swork_id).update(**d)
            StandartWork.objects.get(pk=swork_id).positionsEnable.clear()
            for e in form.cleaned_data["positionsEnable"]:
                StandartWork.objects.get(pk=swork_id).positionsEnable.add(
                    WorkerPosition.objects.get(name=e)
                )
        return HttpResponseRedirect('/constructors/list/standartWork/')

    c = {'equipment_formset': EquipmentFormset(initial=eq.generateDataFromNeedStructs(
        NeedEquipmentType=Equipment.TYPE_EQUIPMENT), prefix='equipment', ),
        'material_formset': MaterialFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_MATERIAL), prefix='material'),
        'detail_formset': DetailFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_DETAIL), prefix='detail', ),
        'assembly_formset': AssemblyFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_ASSEMBLY_UNIT), prefix='assembly', ),
        'swork_formset': StandartWorkFormset(initial=eq.generateDataFromNeedStructs(
            NeedEquipmentType=Equipment.TYPE_STANDART_WORK), prefix='standart_work', ),
        'login_form': LoginForm(),
        'one': '1',
        'form': StandartWorkForm(instance=StandartWork.objects.get(pk=swork_id), prefix="main_form"),
        'eqType': Equipment.TYPE_STANDART_WORK,
    }

    return render(request, "constructors/detail.html", c)


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


def shemesList(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = SchemeForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            code = form.cleaned_data["code"]
            sch = Scheme.objects.create(link = form.cleaned_data["link"],author =  form.cleaned_data["author"] )
            sch.save()
            if (code is not None):
                sch.code = code
                sch.save()

    return render(request, "constructors/shemesList.html", {
        'login_form': LoginForm(),
        'schs': Scheme.objects.all(),
        'one': '1',
        'form': SchemeForm(),
    })



def workReportList(request,area_id):
    return render(request, "constructors/workReportList.html", {
        'login_form': LoginForm(),
        'area_id': area_id,
        'one': '1'
    })
