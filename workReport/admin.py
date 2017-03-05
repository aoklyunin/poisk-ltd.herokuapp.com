# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Worker, Reject, WorkReport, WorkPart, Order

admin.site.register(Worker)
admin.site.register(Reject)
admin.site.register(WorkReport)
admin.site.register(WorkPart)

admin.site.register(Order)