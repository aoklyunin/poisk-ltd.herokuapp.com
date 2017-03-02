# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django.forms import ModelForm, BaseFormSet
from django import forms
from stock.models import MoveEquipment, MoveAssembly, MoveDetail
from workReport.models import Equipment


class NeedEquipmentForm(ModelForm):
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
        super(NeedEquipmentForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['equipment'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cnt', css_class='col-sm-2', ),
            Field('equipment', css_class='col-sm-2'))


class NeedDetailForm(ModelForm):
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
        super(NeedDetailForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['detail'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cnt', css_class='col-sm-2', ),
            Field('detail', css_class='col-sm-2'))


class NeedAssemblyForm(ModelForm):
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
        super(NeedAssemblyForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['assembly'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('cnt', css_class='col-sm-2', ),
            Field('assembly', css_class='col-sm-2'))
