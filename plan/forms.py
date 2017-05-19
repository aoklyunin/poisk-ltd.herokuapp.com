# -*- coding: utf-8 -*-
# модуль с формами
import datetime

from django import forms
from django.forms import ModelForm, Textarea, BaseFormSet

from plan.models import Attestation
from workReport.models import WorkerPosition

class RequiredFormSet(BaseFormSet):
    def clean(self):
        return

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, queryset=None, **kwargs):
        self.queryset = queryset
        self.initial_extra = kwargs.pop('initial', None)
        defaults = {'data': data, 'files': files, 'auto_id': auto_id, 'prefix': prefix}
        defaults.update(kwargs)
        super(RequiredFormSet, self).__init__(**defaults)

class LoginForm(forms.Form):
    # имя пользователя
    username = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': 'Логин'}),
                               label="")
    # пароль
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), label="")

    widgets = {
        'password': forms.PasswordInput(),
    }


def subdict(form,keyset):
    return dict((k, form.cleaned_data[k]) for k in keyset)

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

    # фамилия
    tnumber = forms.IntegerField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 20, 'placeholder': '112'}),
                                 label="Табельный номер")

