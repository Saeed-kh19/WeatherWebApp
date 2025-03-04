import random
from datetime import timedelta

from django.utils import timezone
from faker import Faker
from django.core.management import BaseCommand

from main.models import City, CityWeatherInfo

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(5):
            city_name = fake.city()
            longitude = random.uniform(-180, 180)
            latitude = random.uniform(-90, 90)

            city = City.objects.create(city_name = city_name, longitude = longitude, latitude = latitude)

            temperature_celsius = round(random.uniform(-30.0,50.0),2)

            days_in_past = random.randint(0,30)
            date_submitted = timezone.now() - timedelta(days=days_in_past)

            CityWeatherInfo.objects.create(city = city,temperature_celsius = temperature_celsius, date_submitted = date_submitted)


        self.stdout.write(self.style.SUCCESS('Cities created successfully!'))