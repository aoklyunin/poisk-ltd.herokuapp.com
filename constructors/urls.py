# -*- coding: utf-8 -*-
from django.conf.urls import url

from constructors.views import workReportList, removeEquipment, listStandartWork, listEquipment, detailStandartWork, \
    detailEquipment

urlpatterns = [
    url(r'^reports/$', workReportList),

    url(r'^detail/(?P<equipment_id>[0-9]+)/$', detailEquipment),
    url(r'^detail/standartWork/(?P<swork_id>[0-9]+)/$', detailStandartWork),

    url(r'^list/(?P<equipment_type>[0-9]+)/(?P<area_id>[0-9]+)/$', listEquipment),
    url(r'^list/standartWork/$', listStandartWork),
    url(r'^remove/(?P<equipment_id>[0-9]+)/$', removeEquipment),

]
