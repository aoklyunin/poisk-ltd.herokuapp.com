# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Worker, Equipment, Reject, WorkReport,   StandartWork, WorkPart, Order,StockStruct, AssemblyUnit, \
    Detail

admin.site.register(Worker)
admin.site.register(Reject)
admin.site.register(WorkReport)
admin.site.register(WorkPart)
admin.site.register(StandartWork)
admin.site.register(Equipment)
admin.site.register(Order)
admin.site.register(StockStruct)
admin.site.register(AssemblyUnit)
admin.site.register(Detail)