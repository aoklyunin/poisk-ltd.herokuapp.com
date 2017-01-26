# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from .models import Scheme, Agreement, Customer, Material, Equipment, AssemblyUnits, WorkerPosition, WorkPlace, Worker, \
     Instrument, HardwareEquipment, Reject, WorkReport, Orders, Attestation, StandartWork, WorkPart

admin.site.register(Scheme)
admin.site.register(Agreement)
admin.site.register(Customer)
admin.site.register(Material)
admin.site.register(Equipment)
admin.site.register(AssemblyUnits)
admin.site.register(WorkerPosition)
admin.site.register(WorkPlace)
admin.site.register(Worker)
admin.site.register(Instrument)
admin.site.register(HardwareEquipment)
admin.site.register(Reject)
admin.site.register(WorkReport)
admin.site.register(Orders)
admin.site.register(Attestation)
admin.site.register(WorkPart)
admin.site.register(StandartWork)

