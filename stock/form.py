# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django import forms
from django.forms import ModelForm, BaseFormSet

from stock.models import Extradition


class ExtraditionForm(ModelForm):
    class Meta:
        model = Extradition
        fields = '__all__'
        widgets = {

        }

        labels = {
            'date': '',
            'content_object': '',
            'cnt': '',
        }

        error_messages = {
            'date': {'invalid': ''},
            'content_object': {'invalid': '', 'invalid_choice': ''},
            'cnt': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ExtraditionForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('date', css_class='col-sm-2', ),
            Field('content_object', css_class='col-sm-2'))
