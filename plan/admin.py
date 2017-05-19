# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Agreement,  Attestation, WorkerPosition, Rationale, Customer, InfoText

admin.site.register(Agreement)
admin.site.register(Customer)

admin.site.register(Attestation)
admin.site.register(WorkerPosition)
admin.site.register(Rationale)
admin.site.register(InfoText)
