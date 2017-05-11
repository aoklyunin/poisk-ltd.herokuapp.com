import datetime

from django.forms import formset_factory

from workReport.forms import MyWorkPartForm
from workReport.models import WorkReport

wr = WorkReport.objects.get(pk=8)
d1 = wr.generateWorkPartData()

d = [{'endTime': datetime.time(8, 45), 'startTime': datetime.time(8, 30), 'workPlace': '', 'standartWork': '19',
      'rationale': '', 'comment': ''},
     {'endTime': datetime.time(2, 45), 'startTime': datetime.time(11, 30), 'workPlace': '', 'standartWork': '27',
      'rationale': '', 'comment': ''},
     {'endTime': datetime.time(2, 45), 'startTime': datetime.time(12, 30), 'workPlace': '', 'standartWork': '18',
      'rationale': '', 'comment': ''}]

ReportFormset = formset_factory(MyWorkPartForm, max_num=10)
formset = ReportFormset(initial=d1, prefix="formset")

for form in formset:
    print(">"+form.as_table())
