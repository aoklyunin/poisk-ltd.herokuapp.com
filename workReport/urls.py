# -*- coding: utf-8 -*-
from django.conf.urls import url

from workReport.views import createWorkReport, workReports, workReportPage2, workReportPage1, workReportPage3, \
    workReportPage4, workReportPage5, workReportPage6, workReportPage7, printReport, deleteReport, test

urlpatterns = [
    url(r'^create/$', createWorkReport),
    url(r'^list/$', workReports),
    url(r'^test/$', test),
    url(r'^page1/(?P<workReport_id>[0-9]+)/$', workReportPage1),
    url(r'^page2/(?P<workReport_id>[0-9]+)/$', workReportPage2),
    url(r'^page3/(?P<workReport_id>[0-9]+)/$', workReportPage3),
    url(r'^page4/(?P<workReport_id>[0-9]+)/$', workReportPage4),
    url(r'^page5/(?P<workReport_id>[0-9]+)/$', workReportPage5),
    url(r'^page6/(?P<workReport_id>[0-9]+)/$', workReportPage6),
    url(r'^page7/(?P<workReport_id>[0-9]+)/$', workReportPage7),
    url(r'^print/(?P<workReport_id>[0-9]+)/$', printReport),
    url(r'^delete/(?P<workReport_id>[0-9]+)/$', deleteReport),
]
