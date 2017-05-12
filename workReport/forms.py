# -*- coding: utf-8 -*-
# модуль с формами
import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field
from django import forms
from django.forms import ModelForm, BaseFormSet, Form, ChoiceField, FloatField, CharField, TimeField

from constructors.models import Equipment
from plan.models import Rationale, WorkPlace, Area
from .models import WorkerPosition, Worker, WorkPart, Reject, NeedStruct, WorkReport

from django.db.models.fields import BLANK_CHOICE_DASH


# получить список оборудования
def getCreatedReports():
    reports = []
    for wr in WorkReport.objects.filter(state=WorkReport.STATE_CREATED):
        reports.append([wr.id, str(wr)])

    return reports + BLANK_CHOICE_DASH

# получить список оборудования
def getCloseReports():
    reports = []
    for wr in WorkReport.objects.filter(state=WorkReport.STATE_LEAVED_TO_STOCK):
        reports.append([wr.id, str(wr)])

    return reports + BLANK_CHOICE_DASH


# получить список стандартных работ
def getStandartWorks():
    reports = []
    for wr in Equipment.objects.filter(equipmentType=Equipment.TYPE_STANDART_WORK):
        reports.append([wr.id, str(wr)])

    return reports + BLANK_CHOICE_DASH


# получить список оборудования
def getRationales():
    reports = []
    for wr in Rationale.objects.all():
        reports.append([wr.id, str(wr)])

    return reports + BLANK_CHOICE_DASH


# получить список оборудования
def getWorkPlaces():
    reports = []
    for wr in WorkPlace.objects.all():
        reports.append([wr.id, str(wr)])

    return reports + BLANK_CHOICE_DASH


# форма для выбора одного изделия
class CreatedReportSingleForm(Form):
    report = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(CreatedReportSingleForm, self).__init__(*args, **kwargs)
        self.fields['report'].choices = getCreatedReports()
        self.fields['report'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['report'].widget.attrs['id'] = 'disease'


class CloseReportSingleForm(Form):
    report = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(CloseReportSingleForm, self).__init__(*args, **kwargs)
        self.fields['report'].choices = getCloseReports()
        self.fields['report'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['report'].widget.attrs['id'] = 'disease'


# форма для отчёта
class ReportForm(forms.Form):
    wPos = WorkerPosition.objects.get(name='Контролёр ОТК')
    # ответственный за ВИК
    VIKer = forms.ModelChoiceField(queryset=Worker.objects.filter(position=wPos),
                                   label="Контролёр ОТК", initial=0)
    # составил наряд
    reportMaker = forms.ModelChoiceField(queryset=Worker.objects.all(),
                                         label="Составил наряд", initial=0)
    # проверил наряд
    reportChecker = forms.ModelChoiceField(queryset=Worker.objects.all(),
                                           label="Проверил наряд", initial=0)
    # исполнитель
    worker = forms.ModelChoiceField(queryset=Worker.objects.all(),
                                    label="Исполнитель", initial=0)
    # начальник
    wPos = WorkerPosition.objects.get(name='Начальник участка')
    supervisor = forms.ModelChoiceField(queryset=Worker.objects.filter(position=wPos),
                                        label="Начальник участка", initial=0)
    # кладовщик
    wPos = WorkerPosition.objects.get(name='Кладовщик')
    stockMan = forms.ModelChoiceField(queryset=Worker.objects.filter(position=wPos),
                                      label="Кладовщик", initial=0)

    adate = forms.DateField(initial=datetime.date.today, label='Дата')

    VIKDate = forms.DateField(initial=datetime.date.today, label='Дата ВИК')

    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 20, 'placeholder': 'Что довавить'}),
                           label="Примечание", required=False)

    area = forms.ModelChoiceField(queryset=Area.objects.all(), label='Площадка')

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['VIKer'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['VIKer'].widget.attrs['id'] = 'disease2'
        self.fields['reportMaker'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['reportMaker'].widget.attrs['id'] = 'disease2'
        self.fields['reportChecker'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['reportChecker'].widget.attrs['id'] = 'disease2'
        self.fields['worker'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['worker'].widget.attrs['id'] = 'disease2'
        self.fields['supervisor'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['supervisor'].widget.attrs['id'] = 'disease2'
        self.fields['stockMan'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['stockMan'].widget.attrs['id'] = 'disease2'

        self.fields['adate'].widget.attrs['id'] = 'datepicker'
        self.fields['VIKDate'].widget.attrs['id'] = 'datepicker2'
        self.helper.layout = Layout(
            Div('supervisor', css_class='col-xs-4', ),
            Div('VIKer', css_class='col-xs-4', ),
            Div('reportMaker', css_class=' col-xs-4', ),
            Div('reportChecker', css_class='col-xs-4', ),
            Div('worker', css_class='col-xs-4', ),
            Div('stockMan', css_class=' col-xs-4', ),
            Div('adate', css_class='col-xs-2', ),
            Div('VIKDate', css_class='col-xs-2', ),
            Div('note', css_class='col-xs-8', ),
            Submit('submit', u'Сохранить', css_class='btn btn-primary center-me center-children'),
        )


# форма для выбора одного изделия с кол-вом
class WorkPartForm(Form):
    comment = CharField(label="", max_length=100)
    startTime = TimeField(label="")
    endTime = TimeField(label="")
    standartWork = ChoiceField(label="")
    workPlace = ChoiceField(label="")
    rationale = ChoiceField(label="")

    def __init__(self, *args, **kwargs):
        super(WorkPartForm, self).__init__(*args, **kwargs)
        self.fields['standartWork'].choices = getStandartWorks()
        self.fields['rationale'].choices = getRationales()
        self.fields['workPlace'].choices = getWorkPlaces()

        self.fields['workPlace'].required = False
        self.fields['rationale'].required = False
        self.fields['startTime'].required = False
        self.fields['endTime'].required = False
        self.fields['comment'].required = False
        self.fields['standartWork'].required = False

        self.fields['standartWork'].widget.attrs['class'] = 'js-example-basic-multiple'
        self.fields['standartWork'].widget.attrs['id'] = 'disease2'

        self.fields['startTime'].error_messages['invalid'] = ''
        self.fields['endTime'].error_messages['invalid'] = ''
        self.fields['workPlace'].error_messages['invalid'] = ''
        self.fields['rationale'].error_messages['invalid'] = ''
        self.fields['standartWork'].error_messages['invalid'] = ''
        self.fields['standartWork'].error_messages['invalid_choice'] = ''
        self.fields['comment'].error_messages['invalid'] = ''

        self.fields['startTime'].widget = forms.TimeInput(format='%H:%M')
        self.fields['endTime'].widget = forms.TimeInput(format='%H:%M')
        self.fields['startTime'].widget.attrs['class'] = 'timepicker123'
        self.fields['endTime'].widget.attrs['class'] = 'timepicker123'


class RejectForm(ModelForm):
    class Meta:
        model = Reject
        fields = '__all__'
        widgets = {
        }

        labels = {
            'cnt': '',
            'equipment': '',
            'material': '',

        }

        error_messages = {
            'equipment': {'invalid_choice': ''},
            'material': {'invalid_choice': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RejectForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['equipment'].required = False


class NeedStructForm(ModelForm):
    class Meta:
        model = NeedStruct
        fields = '__all__'
        widgets = {
        }

        labels = {
            'equipment': '',
            'usedCnt': '',
            'getCnt': '',
            'rejectCnt': '',
            'dustCnt': '',
            'remainCnt': '',
        }

        error_messages = {
            'equipment': {'invalid_choice': ''},
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(NeedStructForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['equipment'].required = False
