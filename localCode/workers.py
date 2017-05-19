import csv

from django.contrib.auth.models import User

from localCode.customOperation import transliterate, password_generator
from nop.models import WorkerPosition, Worker, Area

with open('localCode/in/workers.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';')
    for row in spamreader:
        num = row[1]
        fio = row[2].split()
        second_name = fio[0]
        name = fio[1]
        patr = fio[2]
        wpos = row[3]
        area = Area.objects.get(name=row[4])

        if len( WorkerPosition.objects.filter(name=wpos))==0:
            wp = WorkerPosition.objects.create(name=wpos)
        else:
            wp = WorkerPosition.objects.get(name=wpos)

        # генерируем логин на основе имени и фамилии
        username = (transliterate(name[:1]) + transliterate(second_name)).lower()
        # генерируем пароль
        password = password_generator(8)
        # выводим данные по будующему пользователю
        print(transliterate(name) + u" " + transliterate(second_name) + u" " + username + u" " + password)
        try:
            # создаём пользователя
            user = User.objects.create_user(username=username,
                                            email=username+"@gmail.com",
                                            password=password)


            # задаём ему имя и фамилию
            user.first_name = name
            user.last_name = second_name
            # созраняем пользователя
            user.save()

            # создаём работника
            w = Worker.objects.create(user=user, patronymic=patr,
                                  tnumber=num)
            w.area = area
            # сохраняем студента
            w.save()
            w.position.add(wp)

        except:
            print('Не получилось создать опльзователя')
