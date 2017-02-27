from django.shortcuts import render


def addEquipment(request):
    return render(request, "stock/addStockEquipment.html", {

    })


def extradition(request):
    return render(request, "stock/extradition.html", {

    })


def acceptance(request):
    return render(request, "stock/acceptance.html", {

    })


def detailStockEquipment(request,equipment_id):
    return render(request, "stock/detailEquipment.html", {

    })


def equipmentList(request):
    return render(request, "stock/equipmentList.html", {

    })


def equipmentDetail(request):
    return render(request, "stock/detailEquipment.html", {

    })


def detailList(request):
    return render(request, "stock/detailList.html", {

    })


def assemblyList(request):
    return render(request, "stock/assemblyList.html", {

    })
