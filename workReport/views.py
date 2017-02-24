# -*- coding: utf-8 -*-
import datetime
from datetime import time
from django.core.checks import messages
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.forms import formset_factory, BaseFormSet
from django.urls import reverse

from plan.forms import LoginForm
from workReport.forms import ReportForm, WorkPartForm, HardwareEquipmentForm, RejectForm, ExampleFormSetHelper, \
    ProfileForm, LinkForm, BaseLinkFormSet
from workReport.models import WorkReport, WorkPart, StandartWork, HardwareEquipment, Reject, UserLink, Worker, \
    WorkerPosition


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


def workReportPage1(request, workReport_id):
    work_report = WorkReport.objects.get(pk=workReport_id)
    # если post запрос
    if request.method == 'POST':
        # строим форму на основе запроса
        form = ReportForm(request.POST)
        # если форма заполнена корректно
        if form.is_valid():
            work_report.supervisor = form.cleaned_data["supervisor"]
            work_report.VIKer = form.cleaned_data["VIKer"]
            work_report.reportMaker = form.cleaned_data["reportMaker"]
            work_report.reportChecker = form.cleaned_data["reportChecker"]
            work_report.worker = form.cleaned_data["worker"]
            work_report.stockMan = form.cleaned_data["stockMan"]
            work_report.adate = form.cleaned_data["adate"]
            work_report.VIKDate = form.cleaned_data["VIKDate"]
            work_report.note = form.cleaned_data["note"]
            work_report.save()
        data = form.cleaned_data
    else:
        data = {'supervisor': work_report.supervisor,
                'VIKer': work_report.VIKer,
                'reportMaker': work_report.reportMaker,
                'reportChecker': work_report.reportChecker,
                'worker': work_report.worker,
                'stockMan': work_report.stockMan,
                'adate': work_report.adate,
                'VIKDate': work_report.VIKDate,
                'note': work_report.note,
                }
    # возвращаем простое окно регистрации
    return render(request, "workReport/workReportPage1.html", {
        'form': ReportForm(initial=data),
        'login_form': LoginForm(),
        'pk': workReport_id,
    })


def workReportPage2(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    ReportFormset = formset_factory(WorkPartForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            wr.workPart.clear()
            for form in report_formset.forms:
                w, created = WorkPart.objects.get_or_create(startTime=form.cleaned_data["startTime"],
                                                            endTime=form.cleaned_data["endTime"],
                                                            standartWork=form.cleaned_data["standartWork"],
                                                            workPlace=form.cleaned_data["workPlace"],
                                                            rationale=form.cleaned_data["rationale"],
                                                            comment=form.cleaned_data["comment"])
                w.save()
                wr.workPart.add(w)
            for part in wr.workPart.all():
                for h in part.standartWork.hardwareEquipment.all():
                    print(h)
                    wr.planHardware.add(h)

        data = report_formset.cleaned_data
    else:
        data = {
            'form-TOTAL_FORMS': str(len(wr.workPart.all())),
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': ''
        }
        i = 0
        for part in wr.workPart.all():
            data['form-' + str(i) + '-startTime'] = part.startTime.strftime("%H:%M")
            data['form-' + str(i) + '-endTime'] = part.endTime.strftime("%H:%M")
            data['form-' + str(i) + '-standartWork'] = part.standartWork
            if part.workPlace is not None:
                data['form-' + str(i) + '-workPlace'] = part.workPlace
            if part.rationale is not None:
                data['form-' + str(i) + '-rationale'] = part.rationale
            data['form-' + str(i) + '-comment'] = part.comment
            i += 1
        print(data)

    c = {'link_formset': ReportFormset(data),
         'login_form': LoginForm(),
         'caption': 'Выполняемые работы',
         'pk': workReport_id,
         }
    return render(request, 'workReport/workReportFormsetWorkPart.html', c)


def workReportPage3(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    ReportFormset = formset_factory(WorkPartForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            wr.factWorkPart.clear()
            for form in report_formset.forms:
                w, created = WorkPart.objects.get_or_create(startTime=form.cleaned_data["startTime"],
                                                            endTime=form.cleaned_data["endTime"],
                                                            standartWork=form.cleaned_data["standartWork"],
                                                            workPlace=form.cleaned_data["workPlace"],
                                                            rationale=form.cleaned_data["rationale"],
                                                            comment=form.cleaned_data["comment"])
                w.save()
                wr.factWorkPart.add(w)
        data = report_formset.cleaned_data
    else:
        data = {
            'form-TOTAL_FORMS': str(len(wr.factWorkPart.all())),
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': ''
        }
        i = 0
        for part in wr.factWorkPart.all():
            data['form-' + str(i) + '-startTime'] = part.startTime.strftime("%H:%M")
            data['form-' + str(i) + '-endTime'] = part.endTime.strftime("%H:%M")
            data['form-' + str(i) + '-standartWork'] = part.standartWork
            i += 1

    c = {'link_formset': ReportFormset(data),
         'login_form': LoginForm(),
         'caption': 'Фактически выполненные работы',
         'pk': workReport_id,
         }
    return render(request, 'workReport/workReportFormsetWorkPart.html', c)


def workReportPage4(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    ReportFormset = formset_factory(HardwareEquipmentForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            wr.planHardware.clear()
            for form in report_formset.forms:
                w, created = HardwareEquipment.objects.get_or_create(equipment=form.cleaned_data["equipment"],
                                                                     material=form.cleaned_data["material"],
                                                                     usedCnt=form.cleaned_data["usedCnt"],
                                                                     getCnt=form.cleaned_data["getCnt"],
                                                                     rejectCnt=form.cleaned_data["rejectCnt"],
                                                                     dustCnt=form.cleaned_data["dustCnt"],
                                                                     remainCnt=form.cleaned_data["remainCnt"])
                if created:
                    w.save()

                wr.planHardware.add(w)
                print(form.cleaned_data)
            return HttpResponseRedirect('/workReport/page5/' + str(workReport_id) + '/')
    else:
        if wr.planHardware.all().exists():
            data = {
                'form-TOTAL_FORMS': str(len(wr.planHardware.all())),
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': ''
            }
            i = 0
            for part in wr.planHardware.all():
                data['form-' + str(i) + '-equipment'] = part.equipment
                data['form-' + str(i) + '-material'] = part.material
                data['form-' + str(i) + '-usedCnt'] = part.usedCnt
                data['form-' + str(i) + '-getCnt'] = part.getCnt
                data['form-' + str(i) + '-rejectCnt'] = part.rejectCnt
                data['form-' + str(i) + '-dustCnt'] = part.dustCnt
                data['form-' + str(i) + '-remainCnt'] = part.remainCnt
                i += 1
            print(data)
        else:
            data = {
                'form-TOTAL_FORMS': '0',
                'form-INITIAL_FORMS': '1',
                'form-MAX_NUM_FORMS': '',
            }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Плановая выдача оборудования',
         'login_form': LoginForm(),
         'pk': workReport_id,
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormsetWorkPart.html', c)


def workReportPage5(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)

    #  if wr.workPart.all().exists():

    ReportFormset = formset_factory(HardwareEquipmentForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.noPlanHardware.all().exists():
                wr.noPlanHardware.all().delete()
            for form in report_formset.forms:
                w, created = HardwareEquipment.objects.get_or_create(equipment=form.cleaned_data["equipment"],
                                                                     material=form.cleaned_data["material"],
                                                                     usedCnt=form.cleaned_data["usedCnt"],
                                                                     getCnt=form.cleaned_data["getCnt"],
                                                                     rejectCnt=form.cleaned_data["rejectCnt"],
                                                                     dustCnt=form.cleaned_data["dustCnt"],
                                                                     remainCnt=form.cleaned_data["remainCnt"])
                if created:
                    w.save()
                w.save()
                wr.noPlanHardware.add(w)
                print(form.cleaned_data)
            return HttpResponseRedirect('/workReport/page6/' + str(workReport_id) + '/')
    else:
        if wr.noPlanHardware.all().exists():
            data = {
                'form-TOTAL_FORMS': str(len(wr.noPlanHardware.all())),
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': ''
            }
            i = 0
            for part in wr.noPlanHardware.all():
                data['form-' + str(i) + '-equipment'] = part.equipment
                data['form-' + str(i) + '-material'] = part.material
                data['form-' + str(i) + '-usedCnt'] = part.usedCnt
                data['form-' + str(i) + '-getCnt'] = part.getCnt
                data['form-' + str(i) + '-rejectCnt'] = part.rejectCnt
                data['form-' + str(i) + '-dustCnt'] = part.dustCnt
                data['form-' + str(i) + '-remainCnt'] = part.remainCnt
                i += 1
        else:
            data = {
                'form-TOTAL_FORMS': '0',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Внеплановая выдача оборудования',
         'login_form': LoginForm(),
         'pk': workReport_id,
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormsetWorkPart.html', c)


def workReportPage6(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)

    ReportFormset = formset_factory(RejectForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.rejected.all().exists():
                wr.rejected.all().delete()
            for form in report_formset.forms:
                w = Reject.objects.create(
                    # деталь
                    equipment=form.cleaned_data["equipment"],
                    material=form.cleaned_data["material"],
                    cnt=form.cleaned_data["cnt"],
                )
                w.save()
                wr.rejected.add(w)
                print(form.cleaned_data)
            return HttpResponseRedirect('/workReport/page7/' + str(workReport_id) + '/')
    else:
        data = {
            'form-TOTAL_FORMS': '0',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '',
        }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Направлено в изолятор брака',
         'login_form': LoginForm(),
         'pk': workReport_id,
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormsetWorkPart.html', c)


def workReportPage7(request, workReport_id):
    return render(request, 'workReport/workReportFinal.html', {'id': workReport_id})


def test(request):
    user = request.user

    # Create the formset, specifying the form and formset we want to use.
    LinkFormSet = formset_factory(LinkForm, formset=BaseLinkFormSet)

    link_data = [{'anchor': 'a1', 'url': 'href1'},
                 {'anchor': 'a2', 'url': 'href2'}]

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, user=user)
        link_formset = LinkFormSet(request.POST)

        if profile_form.is_valid() and link_formset.is_valid():
            # Save user info
            user.first_name = profile_form.cleaned_data.get('first_name')
            user.last_name = profile_form.cleaned_data.get('last_name')
            user.save()

            # Now save the data for each form in the formset
            new_links = []

            for link_form in link_formset:
                anchor = link_form.cleaned_data.get('anchor')
                url = link_form.cleaned_data.get('url')

                if anchor and url:
                    new_links.append(UserLink(user=user, anchor=anchor, url=url))

            try:
                with transaction.atomic():
                    # Replace the old with the new
                    UserLink.objects.filter(user=user).delete()
                    UserLink.objects.bulk_create(new_links)

                    # And notify our users that it worked
                    messages.success(request, 'You have updated your profile.')

            except IntegrityError:  # If the transaction failed
                messages.error(request, 'There was an error saving your profile.')
                return redirect(reverse('profile-settings'))

    else:
        profile_form = ProfileForm(user=user)
        link_formset = LinkFormSet(initial=link_data)

    context = {
        'profile_form': profile_form,
        'link_formset': link_formset,
    }

    return render(request, 'workReport/workReportFormsetWorkPart.html', context)


def workReports(request):
    return render_to_response('workReport/workReportList.html', {'reports': WorkReport.objects.all()})


def createWorkReport(request):
    w = WorkReport()
    wPos = WorkerPosition.objects.get(name='Контролёр ОТК')
    w.VIKer = Worker.objects.filter(position=wPos).first()
    w.reportMaker = Worker.objects.all().first()
    w.reportChecker = Worker.objects.all().first()
    w.worker = Worker.objects.all().first()
    wPos = WorkerPosition.objects.get(name='Начальник смены')
    w.supervisor = Worker.objects.filter(position=wPos).first()
    wPos = WorkerPosition.objects.get(name='Кладовщик')
    w.stockMan = Worker.objects.filter(position=wPos).first()
    w.save()
    # заявленные работы
    wp = WorkPart.objects.create(startTime=time(hour=8, minute=30),
                                 endTime=time(hour=8, minute=45),
                                 standartWork=StandartWork.objects.get(
                                     text='Получение наряда и ТМЦ для выполнения работ'),
                                 )
    w.workPart.add(wp)
    wp = WorkPart.objects.create(startTime=time(hour=16, minute=45),
                                 endTime=time(hour=17, minute=00),
                                 standartWork=StandartWork.objects.get(text='Уборка рабочего места'),
                                 )
    w.workPart.add(wp)
    # фактически выполненные работы
    wp = WorkPart.objects.create(startTime=time(hour=8, minute=30),
                                 endTime=time(hour=8, minute=45),
                                 standartWork=StandartWork.objects.get(
                                     text='Получение наряда и ТМЦ для выполнения работ'),
                                 )
    w.factWorkPart.add(wp)
    wp = WorkPart.objects.create(startTime=time(hour=16, minute=30),
                                 endTime=time(hour=16, minute=45),
                                 standartWork=StandartWork.objects.get(
                                     text='Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий день, проверка инструмента, сдача ТМЦ'),
                                 )
    w.factWorkPart.add(wp)

    wp = WorkPart.objects.create(startTime=time(hour=16, minute=45),
                                 endTime=time(hour=17, minute=00),
                                 standartWork=StandartWork.objects.get(
                                     text='Уборка рабочего места'),
                                 )
    w.factWorkPart.add(wp)

    return HttpResponseRedirect('/workReport/page1/' + str(w.pk) + '/')


def deleteReport(request, workReport_id):
    WorkReport.objects.filter(pk=workReport_id).delete()

    return HttpResponseRedirect('/workReport/list/')


def printReport(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)
    document = wr.generateDoc()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=report.docx'
    document.save(response)

    return response
