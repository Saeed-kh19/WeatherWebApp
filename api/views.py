from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import difflib

from api.serializers import CitySerializer, CityWeatherSerializer
from main.models import City, CityWeatherInfo


class CityListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    model = City
    context_object_name = 'cities'

    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        context = {'cities': cities}
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class CityWeatherAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if 'city_name' not in request.data:
            return Response({'Error': 'city_name is required!'}, status=400)

        else:
            input_city_name = request.data['city_name'].lower()
            cities = City.objects.all()
            city_names = [city.city_name.lower() for city in cities]

            closest_match = difflib.get_close_matches(input_city_name, city_names, n=1, cutoff=0.8)

            if closest_match:
                city_name = closest_match[0]
                city = City.objects.filter(city_name__iexact=city_name).first()
            else:
                city = None

            if not city:
                return Response({'Error': 'city_name does not exist!'}, status=400)
            else:
                city_weather = CityWeatherInfo.objects.filter(city=city).order_by('-date_submitted').first()
                if not city_weather:
                    return Response({'Error': 'No weather data for this city!'}, status=404)
                else:
                    city_serializer = CitySerializer(city)
                    city_weather_serializer = CityWeatherSerializer(city_weather)

                    return Response({'city': city_serializer.data, 'latest_weather': city_weather_serializer.data})
