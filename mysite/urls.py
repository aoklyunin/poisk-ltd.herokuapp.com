# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin

import plan.views
import plan.auth

# автоопределение администратора
admin.autodiscover()

urlpatterns = [
    # панель администратора
    url(r'^admin/', include(admin.site.urls)),
    # выход из сайта
    url(r'^logout/$', plan.auth.logout_view),
    # регистрация на сайте
    url(r'^register/$', plan.auth.register),
    url(r'^workReports/$', plan.views.workReports),
    url(r'^createWorkReport/$', plan.views.createWorkReport),
    url(r'^generateWorkReport/$', plan.views.generateWorkReport),
    url(r'^workReport/page1/(?P<workReport_id>[0-9]+)/$', plan.views.workReportPage1),
    url(r'^workReport/page2/(?P<workReport_id>[0-9]+)/$', plan.views.workReportPage2),
    url(r'^workReport/page3/(?P<workReport_id>[0-9]+)/$', plan.views.workReportPage3),
    url(r'^workReport/page4/(?P<workReport_id>[0-9]+)/$', plan.views.workReportPage4),
    url(r'^workReport/page5/(?P<workReport_id>[0-9]+)/$', plan.views.workReportPage5),
    url(r'^workReport/page6/(?P<workReport_id>[0-9]+)/$', plan.views.workReportPage6),
    url(r'^workReport/page7/(?P<workReport_id>[0-9]+)/$', plan.views.workReportPage7),
    url(r'^test/$', plan.views.test),
    url(r'^workReport/print/(?P<workReport_id>[0-9]+)/$', plan.views.printReport),
    url(r'^workersView/$', plan.views.workersView),
    url(r'^workerView/(?P<worker_id>[0-9]+)/$', plan.views.workerView),
    url(r'^', plan.auth.index, name='index'),
]
