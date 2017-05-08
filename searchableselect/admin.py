from django.contrib import admin
from django import forms
from searchableselect.widgets import SearchableSelect
from .models import Cat, Food, Person


class CatAdminForm(forms.ModelForm):
    class Meta:
        model = Cat
        exclude = ()
        widgets = {
            'favorite_foods': SearchableSelect(model='searchableselect.Food', search_field='name', many=True, limit=20),
            'owner': SearchableSelect(model='searchableselect.Person', search_field='name', many=False),
        }


class CatAdmin(admin.ModelAdmin):
    form = CatAdminForm


class FoodAdmin(admin.ModelAdmin):
    pass


class PersonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Cat, CatAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Person, PersonAdmin)
