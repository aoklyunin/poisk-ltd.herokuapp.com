# -*- coding: utf-8 -*-
from django.shortcuts import render

from workReport.models import Order

def orderList(request):
    return render(request, 'plan/orders.html',
                  {'orders':
                       Order.objects.all()
                   })

