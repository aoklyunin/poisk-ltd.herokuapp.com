# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Agreement, WorkPlace, Attestation, WorkerPosition, Rationale, Area, Customer, Scheme

admin.site.register(Agreement)
admin.site.register(Customer)
admin.site.register(WorkPlace)
admin.site.register(Attestation)
admin.site.register(WorkerPosition)
admin.site.register(Rationale)
admin.site.register(Area)
admin.site.register(Scheme)
