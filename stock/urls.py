# -*- coding: utf-8 -*-
from django.conf.urls import url

from stock.views import stockBalance, wrExtradition, wrAcceptance, acceptance, providers, index, detailWrExtradition, \
    doWrExtradition, detailWrAcceptance, equipment

urlpatterns = [
    url(r'^stock_balance/(?P<area_id>[0-9]+)/$', stockBalance),
    url(r'^equipment/(?P<area_id>[0-9]+)/$', equipment),
    url(r'^wrExtradition/(?P<area_id>[0-9]+)/$', wrExtradition),
    url(r'^doWrExtradition/(?P<workReport_id>[0-9]+)/$', doWrExtradition),
    url(r'^wrAcceptance/(?P<area_id>[0-9]+)/$', wrAcceptance),
    url(r'^acceptance/(?P<area_id>[0-9]+)/$', acceptance),
    url(r'^detailWrExtradition/(?P<workReport_id>[0-9]+)/$', detailWrExtradition),
    url(r'^detailWrAcceptance/(?P<workReport_id>[0-9]+)/$', detailWrAcceptance),
    url(r'^providers/$', providers),

    url(r'^', index, name='index'),
]
