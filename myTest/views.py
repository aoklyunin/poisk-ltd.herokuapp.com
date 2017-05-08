import simplejson
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from constructors.form import EquipmentListForm
from constructors.models import Equipment
from myTest.models import Book
from stock.form import MoveForm




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


def book_lookup(request):
    # Default return list
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'query'):
            value = request.GET[u'query']
            # Ignore queries shorter than length 3
            if len(value) > 2:
                model_results = Book.objects.filter(name__icontains=value)
                results = [ {x.id :x.name,} for x in model_results ]
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')