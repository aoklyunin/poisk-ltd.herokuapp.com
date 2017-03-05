# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from constructors.models import StandartWork, NeedStruct, Equipment

admin.site.register(StandartWork)
admin.site.register(NeedStruct)
admin.site.register(Equipment)
