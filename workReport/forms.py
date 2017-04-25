# -*- coding: utf-8 -*-
# модуль с формами
import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field
from django import forms
from django.forms import ModelForm, BaseFormSet

from constructors.models import Equipment
from .models import WorkerPosition, Worker, WorkPart, Reject, NeedStruct


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

    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 20, 'placeholder': 'Что довавить'}),
                           label="Примечание", required=False)


    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
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


class WorkPartForm(ModelForm):
    class Meta:
        model = WorkPart
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
            'startTime': forms.TimeInput(format='%H:%M'),
            'endTime': forms.TimeInput(format='%H:%M'),
        }

        labels = {
            'comment': '',
            'startTime': '',
            'endTime': '',
            'standartWork': '',
            'workPlace': '',
            'rationale': '',
        }

        error_messages = {
            'startTime': {'invalid': ''},
            'endTime': {'invalid': ''},
            'workPlace': {'required': ''},
            'rationale': {'invalid': '', 'invalid_choice': ''},
            'standartWork': {'invalid_choice': ''}
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(WorkPartForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['comment'].required = False
        self.fields["standartWork"].queryset = Equipment.objects.filter(equipmentType=Equipment.TYPE_STANDART_WORK)
        self.fields['workPlace'].required = False
        self.fields['rationale'].required = False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('startTime', css_class='col-sm-2', ),
                    Field('endTime', css_class='col-sm-2'),
                    css_class='row'),
                Field('standartWork', css_class='col-sm-2', ),
                Field('workPlace', css_class='col-sm-2', ),
                Field('comment', css_class='col-sm-2', ),
                Field('rationale', css_class='col-sm-2', ),
                css_class='row')
        )


class ExampleFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            Div('standartWork', css_class='col-xs-2', ),
            Div('workPlace', css_class=' col-xs-2', ),
            Div('startTime', css_class='col-xs-2', ),
            Div('endTime', css_class=' col-xs-2', ),
            Div('comment', css_class='col-xs-2', ),
            Div('rationale', css_class='col-xs-2', ),
        )
        self.render_required_fields = True


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
