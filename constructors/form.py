# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.forms import ModelForm

from plan.models import Scheme


class SchemeForm(ModelForm):
    class Meta:
        model = Scheme
        fields = {'author', 'code', 'link'}

        labels = {
            'author': 'Автор',
            'code': 'Шифр',
            'link': 'Ссылка',
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
            'dimension': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(SchemeForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['code'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('author', css_class='col-sm-2', ),
            Field('code', css_class='col-sm-2'),
            Field('link', css_class='col-sm-2'),
        )