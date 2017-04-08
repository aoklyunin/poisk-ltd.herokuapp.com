from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

# список деталей
def reportList(request, area_id):
    return HttpResponseRedirect('/stock/material/list/0/')
