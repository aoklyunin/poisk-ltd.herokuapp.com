# -*- coding: utf-8 -*-
from django.conf.urls import url

from constructors.views import shemesList, index, stockBalance, \
    tehnology, detailEquipment, addEquipment

urlpatterns = [

    # url(r'^equipment/list/(?P<area_id>[0-9]+)/$', equipmentList),
    # url(r'^material/list/(?P<area_id>[0-9]+)/$', materialList),
    # url(r'^detail/list/(?P<area_id>[0-9]+)/$', detailList),
    # url(r'^assembly/list/(?P<area_id>[0-9]+)/$', assemblyList),
    #  url(r'^standartWork/list/$', standartWorkList),
    #  url(r'^shemes/list/$', shemesList),

    # url(r'^detail/remove/(?P<equipment_id>[0-9]+)/$', removeConstructorEquipment),
    #  url(r'^assembly/remove/(?P<equipment_id>[0-9]+)/$', removeConstructorEquipment),
    # url(r'^standartWork/remove/(?P<equipment_id>[0-9]+)/$', removeConstructorEquipment),

    # url(r'^detail/detail/(?P<equipment_id>[0-9]+)/$', detailConstructorEquipment),
    # url(r'^assembly/detail/(?P<equipment_id>[0-9]+)/$', detailConstructorEquipment),
    # url(r'^standartWork/detail/(?P<equipment_id>[0-9]+)/$', detailConstructorEquipment),

    url(r'^tehnology/$', tehnology),
    url(r'^addEquipment/$', addEquipment),
    url(r'^stock_balance/(?P<area_id>[0-9]+)/$', stockBalance),
    url(r'^detail/(?P<eq_id>[0-9]+)/$', detailEquipment),
    url(r'^', index)

    # url(r'^detail/standartWork/(?P<swork_id>[0-9]+)/$', detailStandartWork),

    # url(r'^list/equipment/(?P<equipment_type>[0-9]+)/(?P<area_id>[0-9]+)/$', listEquipment),

    #    url(r'^remove/equipment/(?P<equipment_id>[0-9]+)/$', removeEquipment),
    #   url(r'^remove/standartWork/(?P<swork_id>[0-9]+)/$', removeStandartWork),

]
