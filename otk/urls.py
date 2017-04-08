# -*- coding: utf-8 -*-
from django.conf.urls import url

from otk.views import reportList

urlpatterns = [
    url(r'^report/list/(?P<area_id>[0-9]+)/$', reportList),


]
