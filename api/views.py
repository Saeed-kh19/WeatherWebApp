from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CitySerializer
from main.models import City


class CityListView(APIView):
    model = City
    context_object_name = 'cities'

    def get(self,request,*args,**kwargs):
        cities = City.objects.all()
        context = {'cities': cities}
        return Response(context)


class CityWeatherView(APIView):
    def post(self,request,*args,**kwargs):
        if 'city_name' not in request.data:
            return Response({'Error':'city_name is required!'},status=400)

        else:
            city_name = request.data['city_name']
            cities = City.objects.filter(city_name=city_name)
            serializer_cities = CitySerializer(cities, many=True)
            return Response({'cities': serializer_cities.data})
