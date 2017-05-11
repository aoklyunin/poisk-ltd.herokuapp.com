# -*- coding: utf-8 -*-
from django.conf.urls import url

from workReport.views import createWorkReport, workReports, workReportPage2, workReportPage1, workReportPage3, \
    workReportPage4, workReportPage5, workReportPage6, printReport, deleteReport, index, formReport, equipment, \
    closeReport, otk, detailCratedWorkReport, archive

urlpatterns = [

    url(r'^formReport/$', formReport),
    url(r'^equipment/$', equipment),
    url(r'^closeReport/$', closeReport),
    url(r'^otk/$', otk),
    url(r'^archive/$', archive),
    url(r'^create/$', createWorkReport),
    url(r'^detailCratedWorkReport/(?P<workReport_id>[0-9]+)/$', detailCratedWorkReport),

    url(r'^list/(?P<area_id>[0-9]+)/$', workReports),
    url(r'^page1/(?P<workReport_id>[0-9]+)/$', workReportPage1),
    url(r'^page2/(?P<workReport_id>[0-9]+)/$', workReportPage2),
    url(r'^page3/(?P<workReport_id>[0-9]+)/$', workReportPage3),
    url(r'^page4/(?P<workReport_id>[0-9]+)/$', workReportPage4),
    url(r'^page5/(?P<workReport_id>[0-9]+)/$', workReportPage5),
    url(r'^page6/(?P<workReport_id>[0-9]+)/$', workReportPage6),
    url(r'^print/(?P<workReport_id>[0-9]+)/$', printReport),
    url(r'^delete/(?P<workReport_id>[0-9]+)/$', deleteReport),

    url(r'^', index, name='index'),
]
