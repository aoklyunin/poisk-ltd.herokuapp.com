# -*- coding: utf-8 -*-
# модуль с формами
import datetime

from django import forms
from django.forms import ModelForm, Textarea

from .models import WorkerPosition, Attestation, Worker, WorkPart, StandartWork, WorkPlace, HardwareEquipment, \
    Reject


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
    wPos = WorkerPosition.objects.get(name='Начальник участка')
    supervisor = forms.ModelChoiceField(queryset=Worker.objects.filter(position=wPos),
                                        label="Начальник участка", initial=0)
    # кладовщик
    wPos = WorkerPosition.objects.get(name='Кладовщик')
    stockMan = forms.ModelChoiceField(queryset=Worker.objects.filter(position=wPos),
                                      label="Кладовщик", initial=0)

    adate = forms.DateField(initial=datetime.date.today, label='Дата')

    VIKDate = forms.DateField(initial=datetime.date.today, label='Дата ВИК')

    note = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Что довавить'}),
                           label="Примечание")


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
