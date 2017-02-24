# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from plan.models import Agreement
from plan.models import Customer
from workReport.models import Scheme, Material, Equipment, AssemblyUnits, Order

admin.site.register(Scheme)
admin.site.register(Agreement)
admin.site.register(Customer)
admin.site.register(Material)
admin.site.register(Equipment)
admin.site.register(AssemblyUnits)
admin.site.register(Order)
