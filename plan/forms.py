# -*- coding: utf-8 -*-
# модуль с формами
import datetime

from django import forms
from django.forms import ModelForm, Textarea

from plan.models import Attestation
from workReport.models import WorkerPosition


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

