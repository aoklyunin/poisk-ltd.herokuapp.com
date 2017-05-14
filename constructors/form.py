# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.forms import ModelForm, Form, MultipleChoiceField, ModelMultipleChoiceField, ChoiceField, ModelChoiceField, \
    TextInput, Textarea, CharField, IntegerField, FloatField

from constructors.models import Equipment
from plan.models import Scheme

from django.db.models.fields import BLANK_CHOICE_DASH


# олучить список чертежей
def getShemes():
    shemes = []
    for sh in Scheme.objects.all().order_by('code'):
        shemes.append([sh.id, str(sh)])

    return shemes + BLANK_CHOICE_DASH


# получить список конструкторского оборудования
def getConstructorEquipment():
    equipments = []
    for i in Equipment.CONSTRUCTOR_ENABLED:
        lst = []
        for eq in Equipment.objects.filter(equipmentType=i).order_by('name'):
            lst.append([eq.id, str(eq)])
        equipments.append([Equipment.EQUIPMENT_LABELS[i], lst])

    return equipments + BLANK_CHOICE_DASH


# получить список оборудования
def getEquipment():
    equipments = []
    for i in range(Equipment.EQUIPMENT_TYPE_COUNT):
        lst = []
        for eq in Equipment.objects.filter(equipmentType=i).order_by('name'):
            lst.append([eq.id, str(eq)])
        equipments.append([Equipment.EQUIPMENT_LABELS[i], lst])

    return equipments + BLANK_CHOICE_DASH


# получить список оборудования без стандартных работ
def getEquipmentWithoutSW():
    equipments = []
    for i in range(Equipment.EQUIPMENT_TYPE_COUNT):
        if i != Equipment.TYPE_STANDART_WORK:
            lst = []
            for eq in Equipment.objects.filter(equipmentType=i).order_by('name'):
                lst.append([eq.id, str(eq)])
            equipments.append([Equipment.EQUIPMENT_LABELS[i], lst])

    return equipments + BLANK_CHOICE_DASH


# получить список сотрудников по категориям
def getWorkers():
    workers = []
    for i in range(Equipment.EQUIPMENT_TYPE_COUNT):
        lst = []
        for eq in Equipment.objects.filter(equipmentType=i).order_by('name'):
            lst.append([eq.id, str(eq)])
        workers.append([Equipment.EQUIPMENT_LABELS[i], lst])

    return workers + BLANK_CHOICE_DASH


# форма для выбора нескольких объектов оборудования
class EquipmentListForm(Form):
    equipment = MultipleChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(EquipmentListForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getEquipment()
        self.fields['equipment'].widget.attrs['class'] = 'beautiful-select'
        self.fields['equipment'].widget.attrs['id'] = 'disease'


# форма для выбора нескольких объектов оборудования без стандартных работ
class EquipmentListWithoutSWForm(Form):
    equipment = MultipleChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(EquipmentListWithoutSWForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getEquipmentWithoutSW()
        self.fields['equipment'].widget.attrs['class'] = 'beautiful-select'
        self.fields['equipment'].widget.attrs['id'] = 'equipment'


# форма для выбора нескольких объектов оборудования без стандартных работ
class EquipmentCntWithoutSWForm(Form):
    equipment = ChoiceField(label="")
    cnt = FloatField(label="")

    def __init__(self, *args, **kwargs):
        super(EquipmentCntWithoutSWForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getEquipmentWithoutSW()
        self.fields['equipment'].widget.attrs['class'] = 'beautiful-select'
        self.fields['equipment'].widget.attrs['id'] = 'disease'
        self.fields['equipment'].initial = None
        self.fields['cnt'].initial = 0
        self.fields['equipment'].required = False
        self.fields['cnt'].required = False

# форма для выбора одного изделия
class EquipmentSingleForm(Form):
    equipment = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(EquipmentSingleForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getEquipment()
        self.fields['equipment'].widget.attrs['class'] = 'beautiful-select'
        self.fields['equipment'].widget.attrs['id'] = 'disease'


# форма для выбора одного изделия с кол-вом
class EquipmentSingleWithCtnForm(Form):
    equipment = ChoiceField(label="")
    cnt = FloatField(label="")

    def __init__(self, *args, **kwargs):
        super(EquipmentSingleWithCtnForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getEquipment()
        self.fields['equipment'].widget.attrs['class'] = 'beautiful-select'
        self.fields['equipment'].widget.attrs['id'] = 'disease'

        self.fields['equipment'].initial = None
        self.fields['cnt'].initial = 0
        self.fields['equipment'].required = False
        self.fields['cnt'].required = False


# форма для выбора изделия для редактирования  конструктором
class EquipmentConstructorSingleForm(Form):
    equipment = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(EquipmentConstructorSingleForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getConstructorEquipment()
        self.fields['equipment'].widget.attrs['class'] = 'beautiful-select'
        self.fields['equipment'].widget.attrs['id'] = 'disease'


# форма для добавления новых изделий
class AddEquipmentForm(Form):
    name = CharField(max_length=10000, label="",
                     widget=TextInput(attrs={'placeholder': 'Изделие'}))
    tp = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(AddEquipmentForm, self).__init__(*args, **kwargs)
        self.fields['tp'].choices = Equipment.CONSTRUCTOR_CHOICES


# форма оборудования
class EquipmentConstructorForm(ModelForm):
    equipmentType = ChoiceField(label='Тип')

    class Meta:
        model = Equipment
        fields = {'name', 'duration', 'code', 'scheme', 'needVIK'}
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Изделие'}),
            'duration': TextInput(attrs={'placeholder': '0.5'}),
        }

        labels = {
            'name': 'Название',
            'duration': 'Длительность(час)',
            'code': 'Шифр',
            'scheme': 'Чертежи',
            'needVIK': 'Приёмка ОТК',
            'equipmentType': '',
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
            'duration': {'required': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(EquipmentConstructorForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['scheme'].required = False
        self.fields['duration'].required = False
        self.fields['code'].required = False
        self.fields['needVIK'].required = False
        self.fields['equipmentType'].choices = Equipment.CONSTRUCTOR_CHOICES
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='col-sm-2', ),
            Field('dimension', css_class='col-sm-2'),
            Field('code', css_class='col-sm-2'),
            Field('scheme', css_class='col-sm-2'),
            Field('needVIK', wrapper_class='i-checks'),
        )
        self.fields['scheme'].choices = getShemes()
        self.fields['scheme'].widget.attrs['class'] = 'beautiful-select'
        self.fields['scheme'].widget.attrs['id'] = 'disease2'


# Форма чертежа
class SchemeForm(ModelForm):
    class Meta:
        model = Scheme
        fields = {'author', 'code', 'link'}

        labels = {
            'author': '',
            'code': '',
            'link': '',
        }
        widgets = {
            'link': TextInput(attrs={'placeholder': 'Ссылка'}),
            'code': TextInput(attrs={'placeholder': 'Шифр'}),
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
        #   self.fields['author'].choices = getWorkers()
        self.fields['author'].widget.attrs['class'] = 'beautiful-select'
        self.fields['author'].widget.attrs['id'] = 'disease2'
        self.fields['code'].widget.attrs['placeholder'] = 'Шифр'
        self.fields['link'].widget.attrs['placeholder'] = 'Ссылка'


# форма для выбора одного чертежа
class SchemeSingleForm(Form):
    scheme = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(SchemeSingleForm, self).__init__(*args, **kwargs)
        self.fields['scheme'].choices = getShemes()
        self.fields['scheme'].widget.attrs['class'] = 'beautiful-select'
        self.fields['scheme'].widget.attrs['id'] = 'disease'
