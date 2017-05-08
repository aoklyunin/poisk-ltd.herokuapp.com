# -*- coding: utf-8 -*-
# обработчик адресов сайта
from django.conf.urls import include, url
from django.contrib import admin

import plan.views
import plan.auth

# автоопределение администратора
from myTest.models import BookAutocomplete

admin.autodiscover()

urlpatterns = [
    url(r'^workReport/', include('workReport.urls')),
    url(r'^stock/', include('stock.urls')),
    url(r'^constructors/', include('constructors.urls')),
    # панель администратора
    url(r'^admin/', include(admin.site.urls)),
    # выход из сайта
    url(r'^logout/$', plan.auth.logout_view),
    # регистрация на сайте
    url(r'^register/$', plan.auth.register),
    url(r'^register/$', plan.auth.register),
    url(r'^otk/$', include('otk.urls')),
    url(r'^orders/list/$', plan.views.orderList),
    url('^searchableselect/', include('searchableselect.urls')),
    url(r'^test/', include('myTest.urls')),
    url(
        r'^country-autocomplete/$',
        BookAutocomplete.as_view(),
        name='country-autocomplete',
    ),

    url(r'^', plan.auth.index, name='index'),


]
