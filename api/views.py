from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CitySerializer, CityWeatherSerializer
from main.models import City, CityWeatherInfo


class CityListView(APIView):
    model = City
    context_object_name = 'cities'

    def get(self,request,*args,**kwargs):
        cities = City.objects.all()
        context = {'cities': cities}
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class CityWeatherView(APIView):
    def post(self,request,*args,**kwargs):
        if 'city_name' not in request.data:
            return Response({'Error':'city_name is required!'},status=400)

        else:
            city_name = (request.data['city_name']).lower()
            city = City.objects.filter(city_name=city_name).first()
            if not city:
                return Response({'Error':'city_name does not exist!'},status=400)
            else:
                city_weather = CityWeatherInfo.objects.filter(city=city).order_by('-date_submitted').first()
                if not city_weather:
                    return Response({'Error':'No weather data for this city!'},status=404)
                else:
                    city_serializer = CitySerializer(city)
                    city_weather_serializer = CityWeatherSerializer(city_weather)

                    return Response({'city':city_serializer.data, 'lastest_weather':city_weather_serializer.data})
