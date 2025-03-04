from django.shortcuts import render
from django.views.generic import ListView

from main.models import City


class CityListView(ListView):
    model = City
    context_object_name = 'cities'

    def get(self,request,*args,**kwargs):
        cities = City.objects.all()
        context = {'cities': cities}
        return cities

    