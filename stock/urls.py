# -*- coding: utf-8 -*-
from django.conf.urls import url

from stock.views import addEquipment, equipmentList, detailList, assemblyList, detailStockEquipment, extradition, \
    acceptance

urlpatterns = [
    url(r'^addEquipment/$', addEquipment),
    url(r'^extradition/$', extradition),
    url(r'^acceptance/$', acceptance),
    url(r'^equipment/detail/(?P<equipment_id>[0-9]+)/$', detailStockEquipment),
    url(r'^equipment/list/$', equipmentList),
    url(r'^detail/list/$', detailList),
    url(r'^assembly/list/$', assemblyList),
]
