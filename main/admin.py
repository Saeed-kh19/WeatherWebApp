from django.contrib import admin
from .models import LoggingModel, City, CityWeatherInfo  # Import the models


@admin.register(LoggingModel)
class LoggingModelAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'datetime', 'ipaddress', 'endpoint', 'http_method', 'city_name')

    def get_user(self, obj):
        return obj.user.username if obj.user else "Anonymous"

    get_user.short_description = 'User'


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city_name', 'longitude', 'latitude')


# Register the CityWeatherInfo model
@admin.register(CityWeatherInfo)
class CityWeatherInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'temperature_celsius', 'date_submitted')
    list_filter = ('city', 'date_submitted')
    search_fields = ('city__city_name',)
