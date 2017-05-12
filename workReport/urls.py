# -*- coding: utf-8 -*-
from django.conf.urls import url

from workReport.views import createWorkReport, printReport, deleteReport, index, formReport, equipment, \
    closeReport, otk, detailCratedWorkReport, archive, detailEquipmentWorkReport, calculateEquipment, stockReady, \
    detailCloseWorkReport, doCloseReport

urlpatterns = [

    url(r'^formReport/$', formReport),
    url(r'^equipment/$', equipment),
    url(r'^closeReport/$', closeReport),
    url(r'^otk/$', otk),
    url(r'^archive/$', archive),
    url(r'^create/$', createWorkReport),
    url(r'^detailCratedWorkReport/(?P<workReport_id>[0-9]+)/$', detailCratedWorkReport),
    url(r'^doCloseReport/(?P<workReport_id>[0-9]+)/$', doCloseReport),
    url(r'^detailCloseWorkReport/(?P<workReport_id>[0-9]+)/$', detailCloseWorkReport),
    url(r'^detailEquipmentWorkReport/(?P<workReport_id>[0-9]+)/$', detailEquipmentWorkReport),
    url(r'^calculateEquipment/(?P<workReport_id>[0-9]+)/$', calculateEquipment),
    url(r'^stockReady/(?P<workReport_id>[0-9]+)/$', stockReady),

    url(r'^print/(?P<tp>[0-9]+)/(?P<workReport_id>[0-9]+)/$', printReport),
    url(r'^delete/(?P<workReport_id>[0-9]+)/$', deleteReport),

    url(r'^', index, name='index'),
]
