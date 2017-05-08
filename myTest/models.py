import datetime

import select2
from dal import autocomplete
from django import forms
from django.db import models

from plan.models import Area




# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class BookChoose(models.Model):
    cnt = models.IntegerField(default=0)
    book = models.ManyToManyField(Book)

