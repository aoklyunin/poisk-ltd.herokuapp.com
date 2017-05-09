import simplejson
from django.shortcuts import render
from django.http import HttpResponse

from constructors.form import EquipmentListForm
from constructors.models import Equipment



def test(request):
    if request.method == "POST":
        # строим форму на основе запроса
        form = EquipmentListForm(request.POST, prefix='main_form')
        # если форма заполнена корректно
        if form.is_valid():
            for e in form.cleaned_data['equipment']:
                print(Equipment.objects.get(pk=e))


    template = 'myTest/index.html'
    context = {
        'form': EquipmentListForm(prefix="main_form")
    }
    return render(request, template, context)

