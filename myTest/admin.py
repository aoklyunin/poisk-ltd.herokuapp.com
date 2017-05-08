from django.contrib import admin

# Register your models here.
from myTest.models import Book


class BookAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)