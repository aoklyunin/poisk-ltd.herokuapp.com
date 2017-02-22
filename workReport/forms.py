# -*- coding: utf-8 -*-
# модуль с формами
import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, MultiField, Div, HTML
from django import forms
from django.forms import ModelForm, BaseFormSet

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
            Submit('submit', u'Дальше', css_class='btn btn-primary center-me center-children'),
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
            'comment': 'Комментарий',
            'startTime': 'начало',
            'endTime': 'конец',
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
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('startTime', css_class='col-xs-1', ),
            Div('endTime', css_class='col-xs-1'),
            Div('standartWork', css_class='col-xs-2', ),
            Div('workPlace', css_class='col-xs-2', ),
            Div('comment', css_class='col-xs-2', ),
            Div('rationale', css_class='col-xs-2', ),
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


class LinkForm(forms.Form):
    """
    Form for individual user links
    """
    anchor = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Link Name / Anchor Text',
        }),
        required=False)
    url = forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'URL',
        }),
        required=False)


class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'] = forms.CharField(
            max_length=30,
            initial=self.user.first_name,
            widget=forms.TextInput(attrs={
                'placeholder': 'First Name',
            }))
        self.fields['last_name'] = forms.CharField(
            max_length=30,
            initial=self.user.last_name,
            widget=forms.TextInput(attrs={
                'placeholder': 'Last Name',
            }))

class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        anchors = []
        urls = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                anchor = form.cleaned_data['anchor']
                url = form.cleaned_data['url']

                # Check that no two links have the same anchor or URL
                if anchor and url:
                    if anchor in anchors:
                        duplicates = True
                    anchors.append(anchor)

                    if url in urls:
                        duplicates = True
                    urls.append(url)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique anchors and URLs.',
                        code='duplicate_links'
                    )

                # Check that all links have both an anchor and URL
                if url and not anchor:
                    raise forms.ValidationError(
                        'All links must have an anchor.',
                        code='missing_anchor'
                    )
                elif anchor and not url:
                    raise forms.ValidationError(
                        'All links must have a URL.',
                        code='missing_URL'
                    )