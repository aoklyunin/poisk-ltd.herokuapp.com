# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from dal import autocomplete
from django.forms import ModelForm, BaseFormSet, TextInput
from django import forms
from django_select2.forms import Select2Widget

from myTest.models import Book, BookChoose
from searchableselect.widgets import SearchableSelect

from constructors.models import Equipment
from stock.models import MoveEquipment
from workReport.models import StandartWork


class BookForm(forms.ModelForm):
    book = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=autocomplete.ModelSelect2(url='country-autocomplete')
    )

    class Meta:
        model = BookChoose
        fields = ('__all__')