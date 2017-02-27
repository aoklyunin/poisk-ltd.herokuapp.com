# -*- coding: utf-8 -*-
from django.conf.urls import url

from stock.views import addStockEquipment, equipmentList, equipmentDetail, createStockDetail, detailList, \
    detailDetail, createStockAssembly, assemblyList, assemblyDetail, createStockEquipment

urlpatterns = [
    url(r'^equipment/add/$', addStockEquipment),
    url(r'^equipment/create/$', createStockEquipment),
    url(r'^equipment/list/$', equipmentList),
    url(r'^equipment/detail/(?P<elem_id>[0-9]+)/$', equipmentDetail),
    url(r'^detail/add/$', createStockDetail),
    url(r'^detail/list/$', detailList),
    url(r'^detail/detail/(?P<elem_id>[0-9]+)/$', detailDetail),
    url(r'^assembly/add/$', createStockAssembly),
    url(r'^assembly/list/$', assemblyList),
    url(r'^assembly/detail/(?P<elem_id>[0-9]+)/$', assemblyDetail),

]
