from django.contrib import admin
from .models import LoggingModel, City, CityWeatherInfo  # Import the models

@admin.register(LoggingModel)
class LoggingModelAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'datetime', 'ipaddress', 'endpoint', 'http_method', 'city_name')

    def get_user(self, obj):
        return obj.user.username if obj.user else "Anonymous"
    get_user.short_description = 'User'


# Register the City model
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city_name', 'longitude', 'latitude')  # Show key fields in the admin panel


# Register the CityWeatherInfo model
@admin.register(CityWeatherInfo)
class CityWeatherInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'temperature_celsius', 'date_submitted')  # Show key fields in the admin panel
    list_filter = ('city', 'date_submitted')  # Add filters for easier navigation
    search_fields = ('city__city_name',)  # Allow searching by city name
