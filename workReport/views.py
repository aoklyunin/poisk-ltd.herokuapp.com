from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.forms import formset_factory, BaseFormSet

from plan.forms import LoginForm
from workReport.forms import ReportForm, WorkPartForm, HardwareEquipmentForm, RejectForm
from workReport.models import WorkReport, WorkPart, StandartWork, HardwareEquipment, Reject


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

            # возвращаем простое окно регистрации
            return HttpResponseRedirect('/workReport/page2/' + str(work_report.pk) + '/')
        else:
            data = {'supervisor': form.cleaned_data["supervisor"],
                    'VIKer': form.cleaned_data["VIKer"],
                    'reportMaker': form.cleaned_data["reportMaker"],
                    'reportChecker': form.cleaned_data["reportChecker"],
                    'worker': form.cleaned_data["worker"],
                    'stockMan': form.cleaned_data["stockMan"],
                    'adate': form.cleaned_data["date"],
                    'VIKDate': form.cleaned_data["VIKDate"],
                    'note': form.cleaned_data["note"],
                    }
            return render(request, "plan/workReportPage1.html", {
                'form': ReportForm(data),
                'login_form': LoginForm()
            })
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
            'form': ReportForm(data),
            'login_form': LoginForm()
        })


def workReportPage2(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)

    #  if wr.workPart.all().exists():

    ReportFormset = formset_factory(WorkPartForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.workPart.all().exists():
                wr.workPart.all().delete()
            for form in report_formset.forms:
                w, created = WorkPart.objects.get_or_create(startTime=form.cleaned_data["startTime"],
                                                            endTime=form.cleaned_data["endTime"],
                                                            standartWork=form.cleaned_data["standartWork"],
                                                            workPlace=form.cleaned_data["workPlace"],
                                                            rationale=form.cleaned_data["rationale"]
                                                            )
                if created:
                    w.save()
                wr.workPart.add(w)
            if len(wr.planHardware.all()) == 0:
                for part in wr.workPart.all():
                    for h in part.standartWork.hardwareEquipment.all():
                        h.pk = None
                        h.save()
                        wr.planHardware.add(h)
                        # print(form.cleaned_data)
            return HttpResponseRedirect('/workReport/page3/' + str(workReport_id) + '/')
    else:
        if wr.workPart.all().exists():
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
                i += 1

            print(data)
        else:
            data = {
                'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
                'form-0-startTime': '08:30',
                'form-0-endTime': '08:45',
                'form-1-startTime': '16:45',
                'form-1-endTime': '17:00',
                'form-0-standartWork': StandartWork.objects.get(text='Получение наряда и ТМЦ для выполнения работ'),
                'form-1-standartWork': StandartWork.objects.get(text='Уборка рабочего места')
            }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Выполняемые работы'
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormset.html', c)


def workReportPage3(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)

    ReportFormset = formset_factory(WorkPartForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.factWorkPart.all().exists():
                wr.factWorkPart.all().delete()
            for form in report_formset.forms:
                w, created = WorkPart.objects.get_or_create(startTime=form.cleaned_data["startTime"],
                                                            endTime=form.cleaned_data["endTime"],
                                                            standartWork=form.cleaned_data["standartWork"],
                                                            workPlace=form.cleaned_data["workPlace"],
                                                            rationale=form.cleaned_data["rationale"]
                                                            )
                if created:
                    w.save()
                wr.factWorkPart.add(w)
                # print(form.cleaned_data)
            return HttpResponseRedirect('/workReport/page4/' + str(workReport_id) + '/')
    else:
        if wr.factWorkPart.all().exists():
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

        else:
            data = {
                'form-TOTAL_FORMS': '3',
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
                'form-0-startTime': '08:30',
                'form-0-endTime': '08:45',
                'form-1-startTime': '16:30',
                'form-1-endTime': '16:45',
                'form-2-startTime': '16:45',
                'form-2-endTime': '17:00',
                'form-0-standartWork': StandartWork.objects.get(text='Получение наряда и ТМЦ для выполнения работ'),
                'form-1-standartWork': StandartWork.objects.get(
                    text='Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий день, проверка инструмента, сдача ТМЦ'),
                'form-2-standartWork': StandartWork.objects.get(text='Уборка рабочего места')
            }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Фактически выполненные работы'
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormset.html', c)


def workReportPage4(request, workReport_id):
    wr = WorkReport.objects.get(pk=workReport_id)

    #  if wr.workPart.all().exists():

    ReportFormset = formset_factory(HardwareEquipmentForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST':
        report_formset = ReportFormset(request.POST, request.FILES)
        if report_formset.is_valid():
            if wr.planHardware.all().exists():
                wr.planHardware.all().delete()
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
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': '',
            }
        report_formset = ReportFormset(data)
    c = {'report_formset': report_formset,
         'caption': 'Плановая выдача оборудования'
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormset.html', c)


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
         'caption': 'Внеплановая выдача оборудования'
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormset.html', c)


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
         'caption': 'Направлено в изолятор брака'
         }
    #  c.update(csrf(request))
    return render(request, 'workReport/workReportFormset.html', c)


def workReportPage7(request, workReport_id):
    return render(request, 'workReport/workReportFinal.html', {'id': workReport_id})


def test(request):
    return render_to_response('workReport/test.html', {})


def workReports(request):
    return render_to_response('workReport/workReportList.html', {'reports': WorkReport.objects.all()})


def createWorkReport(request):
    w = WorkReport()
    w.save()
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
