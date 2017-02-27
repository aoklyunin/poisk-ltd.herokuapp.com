# -*- coding: utf-8 -*-
from django.forms.formsets import BaseFormSet, formset_factory
from django.shortcuts import render

from plan.forms import LoginForm
from stock.form import ExtraditionForm
from workReport.views import RequiredFormSet


class RequiredFormSeExtradiont(BaseFormSet):
    def clean(self):
        return

    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False



def addEquipment(request):
    return render(request, "stock/addStockEquipment.html", {

    })


def extradition(request):
    ReportFormset = formset_factory(ExtraditionForm, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            for form in report_formset.forms:
                print (form.cleaned_data)
    else:
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': ''
        }

    c = {'link_formset': ReportFormset(data),
         'login_form': LoginForm(),
         }
    return render(request, 'stock/extradition.html', c)



def acceptance(request):
    return render(request, "stock/acceptance.html", {

    })


def detailStockEquipment(request,equipment_id):
    return render(request, "stock/detailEquipment.html", {

    })


def equipmentList(request):
    return render(request, "stock/equipmentList.html", {

    })


def equipmentDetail(request):
    return render(request, "stock/detailEquipment.html", {

    })


def detailList(request):
    return render(request, "stock/detailList.html", {

    })


def assemblyList(request):
    return render(request, "stock/assemblyList.html", {

    })
