# -*- coding: utf-8 -*-
from django.contrib import admin

from nop.models import WorkPlace
from .models import Worker, Reject, WorkReport, WorkPart, Order

admin.site.register(Worker)
admin.site.register(Reject)
admin.site.register(WorkReport)
admin.site.register(WorkPart)
admin.site.register(WorkPlace)

admin.site.register(Order)