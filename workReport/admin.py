# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from .models import WorkerPosition, WorkPlace, Worker, \
      HardwareEquipment, Reject, WorkReport,  Attestation, StandartWork, WorkPart, Rationale


admin.site.register(WorkerPosition)
admin.site.register(WorkPlace)
admin.site.register(Worker)
admin.site.register(HardwareEquipment)
admin.site.register(Reject)
admin.site.register(WorkReport)
admin.site.register(Attestation)
admin.site.register(WorkPart)
admin.site.register(StandartWork)
admin.site.register(Rationale)
