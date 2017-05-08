# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.forms import ModelForm, Form, MultipleChoiceField, ModelMultipleChoiceField, ChoiceField, ModelChoiceField, \
    TextInput, Textarea, CharField

from constructors.models import Equipment
from plan.models import Scheme


# форма для выбора нескольких объектов оборудования
class EquipmentListForm(Form):
    equipment = MultipleChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(EquipmentListForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = self.templates_as_choices()
        self.fields['equipment'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['equipment'].widget.attrs['id'] = 'disease'

    def templates_as_choices(self):
        templates = []
        for i in range(Equipment.EQUIPMENT_TYPE_COUNT - 1):
            lst = []
            for eq in Equipment.objects.filter(equipmentType=i).order_by('name'):
                lst.append([eq.id, eq.name])
            templates.append([Equipment.EQUIPMENT_LABELS[i], lst])

        return templates


# форма для выбора изделий для редактирования
class EquipmentConstructorSingleForm(Form):
    equipment = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(EquipmentConstructorSingleForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = self.templates_as_choices()
        self.fields['equipment'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['equipment'].widget.attrs['id'] = 'disease'

    def templates_as_choices(self):
        templates = []
        for i in Equipment.CONSTRUCTOR_ENABLED:
            lst = []
            for eq in Equipment.objects.filter(equipmentType=i).order_by('name'):
                lst.append([eq.id, eq.name])
            templates.append([Equipment.EQUIPMENT_LABELS[i], lst])

        return templates


# форма для добавления новых изделий
class AddEquipmentForm(Form):
    name = CharField(max_length=10000, label="",
                     widget=TextInput(attrs={'placeholder': 'Изделие'}))
    tp = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(AddEquipmentForm, self).__init__(*args, **kwargs)
        self.fields['tp'].choices=Equipment.CONSTRUCTOR_CHOICES


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
