from django.db import models

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


