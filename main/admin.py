from django.contrib import admin

from main.models import City, CityWeatherInfo

admin.site.register(City)
admin.site.register(CityWeatherInfo)

# first admin:  username:hi / password:hi