from faker import Faker
from django.core.management import BaseCommand

from main.models import City

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(50):
            city_name = fake.city()
            longitude = fake.longitude()
            latitude = fake.latitude()
            City.objects.create(city_name = city_name, longitude = longitude, latitude = latitude)

        self.stdout.write(self.style.SUCCESS('Cities created successfully!'))