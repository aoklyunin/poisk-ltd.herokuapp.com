# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def generateWorkReport(request,work_repor_id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
   # p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    #p.showPage()
   # p.save()
    return response