from django.http import JsonResponse
from django.views import View
from rest_framework.authtoken.models import Token
from main.models import City, CityWeatherInfo, LoggingModel


class CityListAPIView(View):
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'Error': 'Authentication token is required!'}, status=401)

        token_key = auth_header.split(' ')[1]
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return JsonResponse({'Error': 'Invalid token!'}, status=401)

        cities = City.objects.all().values('id', 'city_name', 'longitude', 'latitude')
        city_list = list(cities)

        LoggingModel.objects.create(
            user=user,
            ipaddress=self.get_client_ip(request),
            endpoint='/api/cities/',
            http_method='get'
        )

        return JsonResponse({'cities': city_list}, status=200)

    def get_client_ip(self, request):
        """Utility function to get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class CityWeatherAPIView(View):
    def get(self, request, city_name, *args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'Error': 'Authentication token is required!'}, status=401)

        token_key = auth_header.split(' ')[1]  # Extract the token key
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            return JsonResponse({'Error': 'Invalid token!'}, status=401)

        try:
            city = City.objects.get(city_name__iexact=city_name)  # Case-insensitive lookup
        except City.DoesNotExist:
            return JsonResponse({'Error': f'City "{city_name}" not found!'}, status=404)

        weather_info = CityWeatherInfo.objects.filter(city=city).values(
            'city__city_name', 'temperature_celsius', 'date_submitted'
        ).first()

        if not weather_info:
            return JsonResponse({'Error': f'No weather data found for city "{city_name}"!'}, status=404)

        return JsonResponse({'weather': weather_info}, status=200)

    def get_client_ip(self, request):
        """Utility function to get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
