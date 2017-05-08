# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django.forms import ModelForm, BaseFormSet, TextInput
from django import forms
from django_select2.forms import Select2Widget

from searchableselect.widgets import SearchableSelect

from constructors.models import Equipment
from stock.models import MoveEquipment


class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = {'name', 'dimension', 'code', 'scheme', 'needVIK'}
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Перчатки'}),
            'dimension': TextInput(attrs={'placeholder': 'пара'}),
        }

        labels = {
            'name': 'Название',
            'dimension': 'Единица измерения',
            'code': 'Шифр',
            'scheme': 'Чертежи',
            'needVIK': 'Приёмка ОТК'
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
            'dimension': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(EquipmentForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['scheme'].required = False
        self.fields['dimension'].required = False
        self.fields['code'].required = False
        self.fields['needVIK'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='col-sm-2', ),
            Field('dimension', css_class='col-sm-2'),
            Field('code', css_class='col-sm-2'),
            Field('sheme', css_class='col-sm-2'),
            Field('needVIK', wrapper_class='i-checks'),
        )


class MoveForm(ModelForm):
    class Meta:
        model = MoveEquipment
        fields = {'cnt', 'equipment'}
        widgets = {
            'equipment': Select2Widget
        }

        labels = {
            'equipment': '',
            'cnt': '',
        }

        error_messages = {
            'equipment': {'invalid': '', 'invalid_choice': ''},
            'cnt': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(MoveForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['equipment'].required = False
        self.fields['cnt'].required = False

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cnt', css_class='col-sm-2', ),
            Field('equipment', css_class='col-sm-2'))


class MoveEquipmentForm(MoveForm):
    def __init__(self, *args, **kwargs):
        super(MoveEquipmentForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(equipmentType=Equipment.TYPE_INSTUMENT)


class MoveMaterialForm(MoveForm):
    def __init__(self, *args, **kwargs):
        super(MoveMaterialForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(equipmentType=Equipment.TYPE_MATERIAL)


class MoveDetailForm(MoveForm):
    def __init__(self, *args, **kwargs):
        super(MoveDetailForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(equipmentType=Equipment.TYPE_DETAIL)


class MoveAssemblyForm(MoveForm):
    def __init__(self, *args, **kwargs):
        super(MoveAssemblyForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(equipmentType=Equipment.TYPE_ASSEMBLY_UNIT)


class MoveStandartWorkForm(MoveForm):
    def __init__(self, *args, **kwargs):
        super(MoveStandartWorkForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(equipmentType=Equipment.TYPE_STANDART_WORK)


