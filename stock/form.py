# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django.forms import ModelForm, BaseFormSet
from django import forms
from stock.models import MoveEquipment, MoveAssembly, MoveDetail
from workReport.models import Equipment


class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = {'name', 'dimension', 'code', 'equipmentType', 'scheme'}
        widgets = {
            forms.Textarea(attrs={'cols': 150, 'rows': 10}),
        }

        labels = {
            'name': 'Название',
            'dimension': 'Единица измерения',
            'code': 'Шифр',
            'equipmentType': 'Тип оборудования(число)',
            'scheme': 'Чертежи',
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
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='col-sm-2', ),
            Field('dimension', css_class='col-sm-2'),
            Field('code', css_class='col-sm-2'),
            Field('equipmentType', css_class='col-sm-2'),
            Field('sheme', css_class='col-sm-2')
        )


class MoveEquipmentForm(ModelForm):
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
        super(MoveEquipmentForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['equipment'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cnt', css_class='col-sm-2', ),
            Field('equipment', css_class='col-sm-2'))


class MoveDetailForm(ModelForm):
    class Meta:
        model = MoveDetail
        fields = {'cnt', 'detail'}
        widgets = {

        }

        labels = {
            'detail': '',
            'cnt': '',
        }

        error_messages = {
            'detail': {'invalid': '', 'invalid_choice': ''},
            'cnt': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(MoveDetailForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['detail'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cnt', css_class='col-sm-2', ),
            Field('detail', css_class='col-sm-2'))


class MoveAssemblyForm(ModelForm):
    class Meta:
        model = MoveAssembly
        fields = {'cnt', 'assembly'}
        widgets = {

        }

        labels = {
            'assembly': '',
            'cnt': '',
        }

        error_messages = {
            'assembly': {'invalid': '', 'invalid_choice': ''},
            'cnt': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(MoveAssemblyForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['assembly'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cnt', css_class='col-sm-2', ),
            Field('assembly', css_class='col-sm-2'))
