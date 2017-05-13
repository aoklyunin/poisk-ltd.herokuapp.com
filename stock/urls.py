# -*- coding: utf-8 -*-
from django.conf.urls import url

from stock.views import stockBalance, wrExtradition, wrAcceptance, acceptance, providers, index, detailWrExtradition, \
    doWrExtradition, detailWrAcceptance, equipment, stockListAll, detailProvider, createProvider, deleteProvider, \
    createEquipment, deleteEquipment, detailEquipment

urlpatterns = [
    url(r'^stock_balance/(?P<area_id>[0-9]+)/$', stockBalance),
    url(r'^stockListAll/(?P<area_id>[0-9]+)/$', stockListAll),

    url(r'^wrExtradition/(?P<area_id>[0-9]+)/$', wrExtradition),
    url(r'^doWrExtradition/(?P<workReport_id>[0-9]+)/$', doWrExtradition),
    url(r'^wrAcceptance/(?P<area_id>[0-9]+)/$', wrAcceptance),
    url(r'^acceptance/(?P<area_id>[0-9]+)/$', acceptance),
    url(r'^detailWrExtradition/(?P<workReport_id>[0-9]+)/$', detailWrExtradition),
    url(r'^detailWrAcceptance/(?P<workReport_id>[0-9]+)/$', detailWrAcceptance),
    url(r'^detailProvider/(?P<provider_id>[0-9]+)/$', detailProvider),
    url(r'^deleteProvider/(?P<provider_id>[0-9]+)/$', deleteProvider),
    url(r'^providers/$', providers),
    url(r'^createProvider/$', createProvider),

    url(r'^equipment/$', equipment),
    url(r'^createEquipment/$', createEquipment),
    url(r'^deleteEquipment/(?P<equipment_id>[0-9]+)/$', deleteEquipment),
    url(r'^detailEquipment/(?P<equipment_id>[0-9]+)/$', detailEquipment),
    url(r'^', index, name='index'),
]
