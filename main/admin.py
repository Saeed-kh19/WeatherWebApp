from django.contrib import admin
from .models import LoggingModel  # Import the model from 'main'

@admin.register(LoggingModel)
class LoggingModelAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'datetime', 'ipaddress', 'endpoint', 'http_method', 'city_name')

    def get_user(self, obj):
        return obj.user.username if obj.user else "Anonymous"
    get_user.short_description = 'User'
