import select2
from dal import autocomplete
from django import forms
from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BookChoose(models.Model):
    cnt = models.IntegerField(default=0)
    book = models.ForeignKey(Book)


class BookAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Book.objects.none()

        qs = Book.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs