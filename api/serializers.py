from rest_framework import serializers

from main.models import City, CityWeatherInfo


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class CityWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityWeatherInfo
        fields = '__all__'