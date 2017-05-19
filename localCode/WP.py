import csv

from django.contrib.auth.models import User

from constructors.models import StockStruct, Equipment
from localCode.customOperation import transliterate, password_generator
from nop.models import WorkerPosition, Worker, Area, WorkPlace

with open('localCode/in/Krasnoe WP.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
        num = row[0].split('.')
        name = row[1]
        sw = row[2].split('.')

        d = {}
        d["name"] = name
        d["department"] = int(num[0])
        d["sector"] = int(num[1])
        d["number"] = int(num[2])

        if len(WorkPlace.objects.filter(**d)) == 0:
            wp = WorkPlace.objects.create(**d)
        else:
            wp = WorkPlace.objects.get(**d)
        wp.area = Area.objects.get(name="Красное село")
        for wwp in row[3].split('.'):
            if len(WorkerPosition.objects.filter(name=wwp)) == 0:
                wPos = WorkerPosition.objects.create(name=wwp)
            else:
                wPos = WorkerPosition.objects.get(name=wwp)
            wp.wpos.add(wPos)
        wp.save()
        print(wp)

        for s in sw:
            if s!="":
                d = {}
                d["equipmentType"] = Equipment.TYPE_STANDART_WORK
                d["name"] = s
                d["dimension"] = "час"
                d["duration"] = 1
                if len(Equipment.objects.filter(**d)) == 0:
                    eq = Equipment.objects.create(**d)
                else:
                    eq = Equipment.objects.get(**d)

                for area in Area.objects.all():
                    s = StockStruct.objects.create(area=area)
                    eq.stockStruct.add(s)
                eq.save()
                eq.workPlaces.add(wp)
                print(eq)
