# -*- coding: utf-8 -*-
from django.conf.urls import url

from stock.views import equipmentList, detailStockEquipment, extradition, \
    acceptance, workReportList, removeStockEquipment
urlpatterns = [
    url(r'^extradition/(?P<area_id>[0-9]+)/$', extradition),
    url(r'^acceptance/(?P<area_id>[0-9]+)/$', acceptance),
    url(r'^equipment/detail/(?P<equipment_id>[0-9]+)/$', detailStockEquipment),
    url(r'^equipment/remove/(?P<equipment_id>[0-9]+)/$', removeStockEquipment),
    url(r'^equipment/list/(?P<area_id>[0-9]+)/$', equipmentList),

    url(r'^material/detail/(?P<equipment_id>[0-9]+)/$', detailStockMaterial),
    url(r'^material/remove/(?P<equipment_id>[0-9]+)/$', removeStockMaterial),
    url(r'^material/list/(?P<area_id>[0-9]+)/$', materialList),
    url(r'^detail/list/(?P<area_id>[0-9]+)/$', detailList),
    url(r'^assembly/list/(?P<area_id>[0-9]+)/$', assemblyList),
#
    url(r'^reports/$', workReportList),
]
