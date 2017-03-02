# -*- coding: utf-8 -*-
from django.conf.urls import url

from stock.views import addEquipment, equipmentList, detailStockEquipment, extradition, \
    acceptance,workReportList, removeStockEquipment

urlpatterns = [
    url(r'^addEquipment/$', addEquipment),
    url(r'^extradition/(?P<area_id>[0-9]+)/$', extradition),
    url(r'^acceptance/(?P<area_id>[0-9]+)/$', acceptance),
    url(r'^equipment/detail/(?P<equipment_id>[0-9]+)/$', detailStockEquipment),
    url(r'^equipment/remove/(?P<equipment_id>[0-9]+)/$', removeStockEquipment),
    url(r'^equipment/list/(?P<area_id>[0-9]+)/$', equipmentList),
    url(r'^reports/$', workReportList),
]
