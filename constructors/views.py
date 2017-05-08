# -*- coding: utf-8 -*-
from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render

from constructors.form import SchemeForm, EquipmentListForm, EquipmentConstructorSingleForm, AddEquipmentForm
from plan.forms import LoginForm, subdict
from plan.models import Area, WorkerPosition, Scheme
from stock.form import EquipmentForm, MoveEquipmentForm, MoveMaterialForm, MoveDetailForm, \
    MoveAssemblyForm, MoveStandartWorkForm
from stock.views import listEquipmentByType
from .models import StockStruct, Equipment


# главная страница конструкторского отдела
def index(request):
    c = {
        'area_id': Area.objects.first().pk,
        'login_form': LoginForm(),
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
                    'area_id': int(area_id),  # иначе не сравнить с id площадки при переборе
                    'login_form': LoginForm(),
                    'lst': lst,
                    'areas': Area.objects.all().order_by('name'),
                }
                return render(request, "constructors/stockList.html", c)

    c = {
        'area_id': int(area_id),  # иначе не сравнить с id площадки при переборе
        'areas': Area.objects.all().order_by('name'),
        'login_form': LoginForm(),
        'form': EquipmentListForm(prefix="main_form")
    }
    return render(request, "constructors/stockBalance.html", c)

# страница конструкторской работы
def constructorsWork(request):
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
        'form': AddEquipmentForm(prefix="main_form")
    }
    return render(request, "constructors/work.html", c)

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
            for area in Area.objects.all():
                s = StockStruct.objects.create(area=area)
                eq.stockStruct.add(s)
            eq.save()
            Equipment.objects.filter(pk=eq.pk).update(**d)
            return HttpResponseRedirect('/constructors/detail/' + str(eq.pk) + '/')
    return HttpResponseRedirect('/constructors/work/')


def detailEquipment(request, eq_id):
    EquipmentFormset = formset_factory(MoveEquipmentForm)

    eq = Equipment.objects.get(pk=eq_id)

    if request.method == 'POST':
        equipment_formset = EquipmentFormset(request.POST, request.FILES, prefix='equipment')
        eq.addFromFormset(equipment_formset, True)
        # строим форму на основе запроса
        form = EquipmentForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        # if form.is_valid():
        # d = subdict(form, ("name", "dimension", "code", "needVIK"))
        # Equipment.objects.filter(pk=equipment_id).update(**d)
        # Equipment.objects.get(pk=equipment_id).scheme.clear()
        # for e in form.cleaned_data["scheme"]:
        #    Equipment.objects.get(pk=equipment_id).scheme.add(
        #        Scheme.objects.get(name=e)
        #   )
        return HttpResponseRedirect('/constructors/work/')

    c = {'equipment_formset': EquipmentFormset(initial=eq.generateDataFromNeedStructs(
        NeedEquipmentType=Equipment.TYPE_INSTUMENT), prefix='equipment', ),
        'login_form': LoginForm(),
        'one': '1',
        'form': EquipmentForm(instance=Equipment.objects.get(pk=eq_id), prefix="main_form"),
        'eqType': eq.equipmentType,
    }
    return render(request, "constructors/detail.html", c)


# список оснастки
def equipmentList(request, area_id):
    return listEquipmentByType(request, area_id, Equipment.TYPE_INSTUMENT, "constructors/equipmentList.html")


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
    return listEquipmentByType(request, 0, Equipment.TYPE_STANDART_WORK, "constructors/standartWorkList.html")


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
        NeedEquipmentType=Equipment.TYPE_INSTUMENT), prefix='equipment', ),
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


def shemesList(request):
    if request.method == 'POST':
        # строим форму на основе запроса
        form = SchemeForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            code = form.cleaned_data["code"]
            sch = Scheme.objects.create(link=form.cleaned_data["link"], author=form.cleaned_data["author"])
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
