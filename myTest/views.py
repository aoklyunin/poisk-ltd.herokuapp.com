import simplejson
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from myTest.form import BookForm
from myTest.models import Book
from stock.form import MoveForm


def test(request):
    template = 'myTest/index.html'
    context = {
        'form': BookForm()
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