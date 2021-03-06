import datetime

from localCode.workReportGenerator import generateReport

rationales = [
        ['2,3', 'Я так захотел'],
        ['3,4,5', 'А это заставили']
    ]
works = [
        ['1', '-', 'Получение наряда и ТМЦ для выполнения работ', '08:30', '08:45'],
        ['2', '1.2.3', 'Изготовление деталей оснастки для сушки лейнеров по прилагаемому чертежу в кол-ве одного '
                       'комплекта', '13:15', '16:15'],
        ['3', '-', 'Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий день,'
                   'проверка инструмента, сдача ТМЦ', '16:15', '16:45'],
        ['4', '1.2.3', 'Уборка рабочего места', '16:45', '17:00'],
    ]

factWorks = [
        ['1', '-', 'Получение наряда и ТМЦ для выполнения работ', '08:30', '08:45'],
        ['2', '1.2.3', 'Изготовление деталей оснастки для сушки лейнеров по прилагаемому чертежу в кол-ве одного '
                       'комплекта', '13:15', '16:15'],
        ['3', '-', 'Отчет о выполненных работах перед РП и ознакомление со сменным нарядом на следующий рабочий'
                   'день, проверка инструмента, сдача ТМЦ ', '16:15', '16:45'],
        ['4', '1.2.3', 'Уборка рабочего места', '16:45', '17:00'],
    ]
note = '''Примечание 1 (обязательное):
    Максимальный срок проведения ВИК (входного контроля) до конца рабочего дня 16.01.2017 г.'''

planEquipment = [
        ['Перчатки х/б', '123', 'пара', '1', '0', '0', '0', '-1'],
        ['Пруток бронза', 'Б132r', 'мм', '200', '0', '0', '0', '-1'],
    ]
nonPlanEquipment = [
        ['asf х/б', '123', 'пара', '1', '0', '0', '0', '-1'],
        ['Пруток бронза', 'Б132r', 'мм', '200', '1', '2', '1', '5'],
    ]
dust = [
        ['хлам 1', '100'],
        ['хлам 2', '500']
    ]
document = generateReport('ШАВ', 'Шанин А.В.', 'Бука А.В', '124', "Головнёв А.К.", datetime.date.today(), 'Токарь',
                              rationales, works, factWorks, 'Шанин А.В.', 'Шанин А.В.', 'Хионин Б.Г.', note,
                              'аттестация отутствует', dust, planEquipment, nonPlanEquipment)


document.save('out/1.docx')