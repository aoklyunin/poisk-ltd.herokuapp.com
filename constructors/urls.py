# -*- coding: utf-8 -*-
from django.conf.urls import url

from constructors.views import shemes, index, stockBalance, \
    tehnology, detailEquipment, addEquipment, deleteConstructorEquipment

urlpatterns = [
    url(r'^shemes/$', shemes),
    url(r'^tehnology/$', tehnology),
    url(r'^addEquipment/$', addEquipment),
    url(r'^stock_balance/(?P<area_id>[0-9]+)/$', stockBalance),
    url(r'^detail/(?P<eq_id>[0-9]+)/$', detailEquipment),
    url(r'^delete/(?P<eq_id>[0-9]+)/$', deleteConstructorEquipment),
    url(r'^', index),
]
