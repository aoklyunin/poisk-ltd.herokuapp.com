# -*- coding: utf-8 -*-
from django.conf.urls import url

from constructors.views import workReportList, addDetail, addAssembly, detailDetail, detailAssembly, addStandartWork, \
    detailStandartWork, listDetail, listAssembly, listStandartWork

urlpatterns = [
    url(r'^reports/$', workReportList),
    url(r'^add/detail/$', addDetail),
    url(r'^add/assembly/$', addAssembly),
    url(r'^add/standartWork/$', addStandartWork),
    url(r'^detail/detail/(?P<detail_id>[0-9]+)/$', detailDetail),
    url(r'^detail/assembly/(?P<assembly_id>[0-9]+)/$', detailAssembly),
    url(r'^detail/detail/(?P<detail_id>[0-9]+)/$', detailStandartWork),
    url(r'^list/detail/(?P<detail_id>[0-9]+)/$', listDetail),
    url(r'^list/assembly/(?P<assembly_id>[0-9]+)/$', listAssembly),
    url(r'^list/detail/(?P<detail_id>[0-9]+)/$', listStandartWork),
]
