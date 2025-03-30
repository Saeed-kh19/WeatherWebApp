# from django.contrib.auth.models import User
# from django.shortcuts import render
# from django.views.generic import ListView
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.models import Token
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView
# import difflib
#
# from api.serializers import CitySerializer, CityWeatherSerializer
# from main.models import City, CityWeatherInfo
#
#
# class CityListAPIView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     model = City
#     context_object_name = 'cities'
#
#     def get(self, request, *args, **kwargs):
#         cities = City.objects.all()
#         context = {'cities': cities}
#         serializer = CitySerializer(cities, many=True)
#         return Response(serializer.data)
#
#
# class CityWeatherAPIView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         if 'city_name' not in request.data:
#             return Response({'Error': 'city_name is required!'}, status=400)
#
#         else:
#             input_city_name = request.data['city_name'].lower()
#             cities = City.objects.all()
#             city_names = [city.city_name.lower() for city in cities]
#
#             closest_match = difflib.get_close_matches(input_city_name, city_names, n=1, cutoff=0.8)
#
#             if closest_match:
#                 city_name = closest_match[0]
#                 city = City.objects.filter(city_name__iexact=city_name).first()
#             else:
#                 city = None
#
#             if not city:
#                 return Response({'Error': 'city_name does not exist!'}, status=400)
#             else:
#                 city_weather = CityWeatherInfo.objects.filter(city=city).order_by('-date_submitted').first()
#                 if not city_weather:
#                     return Response({'Error': 'No weather data for this city!'}, status=404)
#                 else:
#                     city_serializer = CitySerializer(city)
#                     city_weather_serializer = CityWeatherSerializer(city_weather)
#
#                     return Response({'city': city_serializer.data, 'latest_weather': city_weather_serializer.data})
#
# # class LoginAPIView(APIView):
# #     def post(self,request,*args,**kwargs):
# #         username = request.data.get("username")
# #         email = request.data.get("email")
# #
# #         if not username or not email:
# #             return Response({'Error': 'username and email is required!'}, status=400)
# #         try:
# #             user = User.objects.get(username__iexact=username,email__iexact=email)
# #             if Token.objects.filter(user=user).exists():
# #                 token = Token.objects.get(user=user)
# #             else:
# #                 token = Token.objects.create(user=user)
# #             return Response({'token': token.key})
# #         except User.DoesNotExist:
# #             return Response({'Error': 'username or email is invalid!'}, status=400)
# #     def get(self,request,*args,**kwargs):
# #         return render(request,'index.html')

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

        # Log the request
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
        # Step 1: Retrieve the token from the Authorization header
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'Error': 'Authentication token is required!'}, status=401)

        token_key = auth_header.split(' ')[1]  # Extract the token key
        try:
            token = Token.objects.get(key=token_key)
            user = token.user  # Verify the token corresponds to a valid user
        except Token.DoesNotExist:
            return JsonResponse({'Error': 'Invalid token!'}, status=401)

        # Step 2: Find the city by its name (case-insensitive)
        try:
            city = City.objects.get(city_name__iexact=city_name)  # Case-insensitive lookup
        except City.DoesNotExist:
            return JsonResponse({'Error': f'City "{city_name}" not found!'}, status=404)

        # Step 3: Retrieve weather information for the city
        weather_info = CityWeatherInfo.objects.filter(city=city).values(
            'city__city_name', 'temperature_celsius', 'date_submitted'
        ).first()

        if not weather_info:
            return JsonResponse({'Error': f'No weather data found for city "{city_name}"!'}, status=404)

        # Step 4: Return the weather data
        return JsonResponse({'weather': weather_info}, status=200)


    def get_client_ip(self, request):
        """Utility function to get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
