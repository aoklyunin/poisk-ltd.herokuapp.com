# -*- coding: utf-8 -*-
from django.contrib import admin

from stock.models import MoveEquipment, MoveDetail, MoveAssembly

admin.site.register(MoveEquipment)
admin.site.register(MoveDetail)
admin.site.register(MoveAssembly)