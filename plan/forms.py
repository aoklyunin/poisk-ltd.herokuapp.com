# -*- coding: utf-8 -*-
# модуль с формами
import datetime

from django import forms
from django.forms import ModelForm, Textarea

from plan.models import WorkerPosition, Attestation, Worker, WorkPart, StandartWork, WorkPlace


class LoginForm(forms.Form):
    # имя пользователя
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Логин'}),
                               label="")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label="")

    widgets = {
        'password': forms.PasswordInput(),
    }


# форма регистрации
class RegisterForm(forms.Form):
    # логин
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'mylogin'}),
                               label="Логин")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
                               label="Пароль")
    # повтор пароля
    rep_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'rows': 1, 'cols': 20, 'placeholder': 'qwerty123'}),
        label="Повторите пароль")
    # почта
    mail = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'example@gmail.com'}),
                           label="Адрес электронной почты")
    # имя
    name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иван'}), label="Имя")
    # фамилия
    second_name = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иванов'}),
                                  label="Фамилия")
    # отчество
    patronymic = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Иванович'}),
                                 label="Отчество")

    # должность
    position = forms.ModelMultipleChoiceField(queryset=WorkerPosition.objects.all())

    # аттестации
    attestation = forms.ModelMultipleChoiceField(queryset=Attestation.objects.all(), required=False)

    # фамилия
    tnumber = forms.IntegerField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': '112'}),
                                 label="Табельный номер")


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


    # document = generateReport('ШАВ', 'Шанин А.В.', 'Бука А.В', '124', "Головнёв А.К.",
    #                           datetime.date.today(), 'Токарь',
    #                          rationales, works, factWorks,
    #                          'Шанин А.В.', 'Шанин А.В.', 'Хионин Б.Г.',
    #                          note,
    #                           'аттестация отутствует', dust, planEquipment, nonPlanEquipment)


class WorkPartForm(ModelForm):
    class Meta:
        model = WorkPart
        fields = '__all__'
        # comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 20, 'placeholder': 'Комментарий'}),
        #                         label="Комментарий", required=False)
        # startTime = forms.TimeField(label='Время начала', initial=datetime.time(12, 30), required=False)
        # endTime = forms.TimeField(label='Время конца', required=False)
        # standartWork = forms.ModelChoiceField(queryset=StandartWork.objects.all(), label='Работа', required=False)
        # workPlace = forms.ModelChoiceField(queryset=WorkPlace.objects.all(), label='Рабочее место', required=False)
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
            'workPlace': 'Рабочее место',
            'rationale': 'Обоснование',
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


class ReportFormPage2(forms.Form):
    pass
