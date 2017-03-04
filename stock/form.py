# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django.forms import ModelForm, BaseFormSet, TextInput
from django import forms
from stock.models import MoveEquipment
from workReport.models import Equipment, StandartWork


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


class StandartWorkForm(ModelForm):
    class Meta:
        model = StandartWork
        fields = {'text', 'positionsEnable', 'duration', 'needVIK'}
        widgets = {
            'text': TextInput(attrs={'placeholder': 'Работа'}),
        }

        labels = {
            'text': 'Название',
            'positionsEnable': 'Должности',
            'duration': 'длительность',
            'needVIK': 'Приёмка ОТК'
        }

        error_messages = {
            'positionsEnable': {'invalid': '', 'invalid_choice': ''},
            'text': {'required': ''},
            'duration': {'required': ''},
            'needVIK': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(StandartWorkForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['duration'].required = False
        self.fields['positionsEnable'].required = False
        self.fields['needVIK'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('positionsEnable', css_class='col-sm-2', ),
            Field('text', css_class='col-sm-2'),
            Field('needVIK', css_class='col-sm-2'),
            Field('duration', css_class='col-sm-2'),
        )


class MoveForm(ModelForm):
    class Meta:
        model = MoveEquipment
        fields = {'cnt', 'equipment'}
        widgets = {

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

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cnt', css_class='col-sm-2', ),
            Field('equipment', css_class='col-sm-2'))


class MoveEquipmentForm(MoveForm):
    def __init__(self, *args, **kwargs):
        super(MoveEquipmentForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(equipmentType=Equipment.TYPE_EQUIPMENT)


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
