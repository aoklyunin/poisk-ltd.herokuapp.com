# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import ModelForm, TextInput, ChoiceField, Form, FloatField, CharField, ModelChoiceField, \
    MultipleChoiceField, Textarea

from constructors.form import getShemes
from constructors.models import Equipment
from stock.models import Provider
from workReport.forms import ReportSingleForm, getReport
from workReport.models import WorkReport, StockReportStruct


# форма для выбора одного изделия
class StockReadyReportSingleForm(ReportSingleForm):
    def __init__(self, *args, **kwargs):
        super(StockReadyReportSingleForm, self).__init__(*args, **kwargs)
        self.fields['report'].choices = getReport(WorkReport.STATE_STOCK_READY)


# форма для выбора одного наряда после приёмки на складе
class StockLeaveReportSingleForm(ReportSingleForm):
    def __init__(self, *args, **kwargs):
        super(StockLeaveReportSingleForm, self).__init__(*args, **kwargs)
        self.fields['report'].choices = getReport(WorkReport.STATE_GETTED_FROM_STOCK)


# форма для приёмки оборудования по наряду
class StockLeaveReportForm(Form):
    # брак
    rejectCnt = FloatField(initial=0, label="")
    # утиль
    dustCnt = FloatField(initial=0, label="")
    # возвращено
    returnCnt = FloatField(initial=0, label="")
    # структура склада (по факту нужно только для связи с полем оборужования, отвечающим за хранение на складе)
    ss = ModelChoiceField(queryset=StockReportStruct.objects.all())
    # оборудование (по факту нужно только для отображения на странице названия)
    equipment = CharField(initial="", label="")
    # получено
    cnt = FloatField(initial="", label="")

    def __init__(self, *args, **kwargs):
        super(StockLeaveReportForm, self).__init__(*args, **kwargs)
        self.fields['ss'].required = False
        self.fields['ss'].widget.attrs['class'] = 'hidden'
        self.fields['equipment'].required = False
        self.fields['ss'].required = False
        self.fields['cnt'].required = False
        self.fields['returnCnt'].required = False


# получить список оборудования без стандартных работ
def getStockEquipment():
    equipments = []
    for i in [Equipment.TYPE_INSTUMENT, Equipment.TYPE_MATERIAL]:
        lst = []
        for eq in Equipment.objects.filter(equipmentType=i).order_by('name'):
            lst.append([eq.id, str(eq)])
        equipments.append([Equipment.EQUIPMENT_LABELS[i], lst])

    return equipments + BLANK_CHOICE_DASH


# форма для выбора нескольких объектов оборудования
class StockEquipmentListForm(Form):
    equipment = MultipleChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(StockEquipmentListForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getStockEquipment()
        self.fields['equipment'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['equipment'].widget.attrs['id'] = 'disease'


# форма для выбора нескольких объектов оборудования без стандартных работ
class StockEquipmentCntForm(Form):
    equipment = ChoiceField(label="")
    cnt = FloatField(label="")

    def __init__(self, *args, **kwargs):
        super(StockEquipmentCntForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getStockEquipment()
        self.fields['equipment'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['equipment'].widget.attrs['id'] = 'disease'
        self.fields['equipment'].initial = None
        self.fields['cnt'].initial = 0
        self.fields['equipment'].required = False
        self.fields['cnt'].required = False


# форма для выбора нескольких объектов оборудования без стандартных работ
class StockEquipmentCntForm(Form):
    equipment = ChoiceField(label="")
    cnt = FloatField(label="")

    def __init__(self, *args, **kwargs):
        super(StockEquipmentCntForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = getStockEquipment()
        self.fields['equipment'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['equipment'].widget.attrs['id'] = 'disease'
        self.fields['equipment'].initial = None
        self.fields['cnt'].initial = 0
        self.fields['equipment'].required = False
        self.fields['cnt'].required = False


# форма для редактирования оборудования
class EquipmentForm(ModelForm):
    equipmentType = ChoiceField(label='Тип')

    class Meta:
        model = Equipment
        # поля
        fields = {'name', 'dimension', 'code', 'scheme', 'needVIK'}
        # виджеты
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Изделие'}),
            'dimension': TextInput(attrs={'placeholder': 'шт.'}),
        }

        labels = {
            'name': 'Название',
            'dimension': 'Единица измерения',
            'code': 'Шифр',
            'scheme': 'Чертежи',
            'needVIK': 'Приёмка ОТК',
            'equipmentType': '',
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
        self.fields['scheme'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['scheme'].widget.attrs['id'] = 'disease2'


# форма для добавления новых изделий
class AddProviderForm(Form):
    name = CharField(max_length=10000, label="",
                     widget=TextInput(attrs={'placeholder': 'Название фирмы'}))

    def __init__(self, *args, **kwargs):
        super(AddProviderForm, self).__init__(*args, **kwargs)


# олучить список чертежей
def getProviders():
    providers = []
    for sh in Provider.objects.all().order_by('name'):
        providers.append([sh.id, str(sh)])

    return providers + BLANK_CHOICE_DASH


# форма для выбора изделия для редактирования  конструктором
class ProviderSingleForm(Form):
    provider = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(ProviderSingleForm, self).__init__(*args, **kwargs)
        self.fields['provider'].choices = getProviders()
        self.fields['provider'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['provider'].widget.attrs['id'] = 'disease'


# поставщик
class ProviderForm(ModelForm):
    class Meta:
        model = Provider
        # поля
        fields = {'name', 'mail', 'contactPerson', 'tel', 'comment'}
        # виджеты
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Рога и Копыта'}),
            'mail': TextInput(attrs={'placeholder': 'roga&copita@mail.ru'}),
            'contactPerson': TextInput(attrs={'placeholder': 'Василий Пупкин'}),
            'tel': TextInput(attrs={'placeholder': '8 800 555 35 35'}),
            'comment': Textarea(attrs={'rows': 2, 'cols': 20, 'placeholder': 'Дополнительные данные'}),
        }

        labels = {
            'name': 'Название Фирмы',
            'contactPerson': 'Контактное лицо',
            'tel': 'Телефон',
            'comment': 'Комментарий',
            'mail': 'Почта',
        }

        error_messages = {
            'name': {'invalid': '', 'invalid_choice': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ProviderForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['name'].required = False
        self.fields['mail'].required = False
        self.fields['contactPerson'].required = False
        self.fields['tel'].required = False
        self.fields['comment'].required = False
