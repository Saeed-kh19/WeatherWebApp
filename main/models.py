from django.db import models
from rest_framework.authtoken.admin import User


class City(models.Model):
    city_name = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.city_name


class CityWeatherInfo(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature_celsius = models.FloatField()
    date_submitted = models.DateTimeField(auto_now_add=True)


class LoggingModel(models.Model):
    METHOD_CHOICES = [
        ('post', 'POST'),
        ('get', 'GET'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    ipaddress = models.GenericIPAddressField()
    endpoint = models.URLField(max_length=200)
    http_method = models.CharField(choices=METHOD_CHOICES,default='get',max_length=5)
    city_name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        if self.user:
            username = self.user.username
        else:
            username = "Not Authenticated User!!"
        return f'{username} - {self.datetime}'