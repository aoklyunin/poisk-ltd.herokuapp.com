# -*- coding: utf-8 -*-
# модуль с формами
import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, MultiField, Div
from django import forms
from django.forms import ModelForm

from .models import WorkerPosition, Worker, WorkPart, HardwareEquipment, Reject


# форма для отчёта
class ReportForm(forms.Form):
    wPos = WorkerPosition.objects.get(name='Контролёр ОТК')
    # ответственный за ВИК
    VIKer = forms.ModelChoiceField(queryset=Worker.objects.filter(position=wPos),
                                   label="Контроллёр ОТК", initial=0)
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
    wPos = WorkerPosition.objects.get(name='Начальник смены')
    supervisor = forms.ModelChoiceField(queryset=Worker.objects.filter(position=wPos),
                                        label="Начальник участка", initial=0)
    # кладовщик
    wPos = WorkerPosition.objects.get(name='Кладовщик')
    stockMan = forms.ModelChoiceField(queryset=Worker.objects.filter(position=wPos),
                                      label="Кладовщик", initial=0)

    adate = forms.DateField(initial=datetime.date.today, label='Дата')

    VIKDate = forms.DateField(initial=datetime.date.today, label='Дата ВИК')

    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Что довавить'}),
                           label="Примечание",required=False    )

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('supervisor', style="background: white;", title="Explication title", css_class="bigdivs"),
            Div('VIKer', style="background: white;", title="Explication title", css_class="bigdivs"),
            Div('reportMaker', style="background: white;", title="Explication title", css_class="bigdivs"),
            Div('reportChecker', style="background: white;", title="Explication title", css_class="bigdivs"),
            Div('worker', style="background: white;", title="Explication title", css_class="bigdivs"),
            Div('stockMan', style="background: white;", title="Explication title", css_class="bigdivs"),
            Div('note', style="background: white;", title="Explication title", css_class="bigdivs"),
            Div(
                Div('adate', css_class='col-md-6', ),
                Div('VIKDate', css_class='col-md-6', ),
                css_class='row',
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
            )
        )

class WorkPartForm(ModelForm):
    class Meta:
        model = WorkPart
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'startTime': forms.TimeInput(format='%H:%M'),
            'endTime': forms.TimeInput(format='%H:%M'),
        }

        labels = {
            'comment': 'Комментарий',
            'startTime': 'Время начала работы',
            'endTime': 'Время конца работы',
            'standartWork': 'Работа',
            # 'workPlace': 'Рабочее место',
            # 'rationale': 'Обоснование',
        }

        error_messages = {
            'startTime': {'invalid': 'Укажите корректное время'},
            'endTime': {'invalid': 'Укажите корректное время'},
            'standartWork': {'required': 'Это поле необходимо для заполнения'}
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(WorkPartForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['comment'].required = False
        self.fields['workPlace'].required = False
        self.fields['rationale'].required = False


class RejectForm(ModelForm):
    class Meta:
        model = Reject
        fields = '__all__'
        widgets = {
        }

        labels = {
            'equipment': 'оборудование',
            'usedCnt': 'использовано',
            'сnt': 'кол-во',
        }

        error_messages = {
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(RejectForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['equipment'].required = False
        self.fields['material'].required = False


class WorkPartForm(ModelForm):
    class Meta:
        model = WorkPart
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
            'startTime': forms.TimeInput(format='%H:%M'),
            'endTime': forms.TimeInput(format='%H:%M'),
        }

        labels = {
            'comment': 'Комментарий',
            'startTime': 'Время начала работы',
            'endTime': 'Время конца работы',
            'standartWork': 'Работа',
            # 'workPlace': 'Рабочее место',
            # 'rationale': 'Обоснование',
        }

        error_messages = {
            'startTime': {'invalid': 'Укажите корректное время'},
            'endTime': {'invalid': 'Укажите корректное время'},
            'standartWork': {'required': 'Это поле необходимо для заполнения'}
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(WorkPartForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['comment'].required = False
        self.fields['workPlace'].required = False
        self.fields['rationale'].required = False


class HardwareEquipmentForm(ModelForm):
    class Meta:
        model = HardwareEquipment
        fields = '__all__'
        widgets = {
        }

        labels = {
            'equipment': 'оборудование',
            'usedCnt': 'использовано',
            'getCnt': 'получено',
            'rejectCnt': 'брак',
            'dustCnt': 'утиль',
            'remainCnt': 'осталось',
        }

        error_messages = {
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(HardwareEquipmentForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['equipment'].required = False
        self.fields['material'].required = False
