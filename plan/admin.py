# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from .models import Scheme, Agreement, Customer, Material, Equipment, AssemblyUnits, Instrument,Orders

admin.site.register(Scheme)
admin.site.register(Agreement)
admin.site.register(Customer)
admin.site.register(Material)
admin.site.register(Equipment)
admin.site.register(AssemblyUnits)
admin.site.register(Orders)
admin.site.register(Instrument)

