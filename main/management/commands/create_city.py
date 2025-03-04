import Faker
from django.core.management import BaseCommand

from main.models import City

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(50):
            city_name =