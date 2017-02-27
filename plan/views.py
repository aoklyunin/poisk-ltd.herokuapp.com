# -*- coding: utf-8 -*-
from django.shortcuts import render

from workReport.models import Order, AssemblyUnit


def orderList(request):
    return render(request, 'plan/orders.html',
                  {'orders':
                       Order.objects.all()
                   })


def assemlyUnitList(request):
    return render(request, 'plan/assembly_units.html',
                  {'assembly_units':
                       AssemblyUnit.objects.all()
                   })
