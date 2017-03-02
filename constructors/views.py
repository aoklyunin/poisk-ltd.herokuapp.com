from django.shortcuts import render

# Create your views here.



def workReportList(request):
    return render(request, "constructors/workReportList.html", {

    })

def addDetail(request):
    return render(request, "constructors/add.html", {

    })

def addAssembly(request):
    return render(request, "constructors/workReportList.html", {

    })

def addStandartWork(request):
    return render(request, "constructors/workReportList.html", {

    })

def detailDetail(request,assembly_id):
    return render(request, "constructors/detail.html", {

    })

def detailAssembly(request,assembly_id):
    return render(request, "constructors/workReportList.html", {

    })

def detailStandartWork(request,assembly_id):
    return render(request, "constructors/workReportList.html", {

    })