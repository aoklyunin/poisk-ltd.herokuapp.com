from nop.models import WorkPlace, Area

for wp in WorkPlace.objects.filter(department__lte=18):
    wp.area = Area.objects.get(name="Красное село")
    wp.save()

for wp in WorkPlace.objects.filter(department__gt=18):
    wp.area = Area.objects.get(name="Малахит")
    wp.save()
