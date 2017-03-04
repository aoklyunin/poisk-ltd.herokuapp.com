# -*- coding: utf-8 -*-
from django.conf.urls import url

from constructors.views import workReportList, removeEquipment, listStandartWork, listEquipment, detailStandartWork, \
    detailEquipment, removeStandartWork

urlpatterns = [
    url(r'^reports/$', workReportList),
    url(r'^detail/equipment/(?P<equipment_id>[0-9]+)/$', detailEquipment),
    url(r'^detail/standartWork/(?P<swork_id>[0-9]+)/$', detailStandartWork),

    url(r'^list/equipment/(?P<equipment_type>[0-9]+)/(?P<area_id>[0-9]+)/$', listEquipment),
    url(r'^list/standartWork/$', listStandartWork),
    url(r'^remove/equipment/(?P<equipment_id>[0-9]+)/$', removeEquipment),
    url(r'^remove/standartWork/(?P<swork_id>[0-9]+)/$', removeStandartWork),

]
