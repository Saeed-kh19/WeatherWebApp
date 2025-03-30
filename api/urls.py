from django.urls import path
from api.views import CityListAPIView, CityWeatherAPIView

urlpatterns = [
    path('cities/', CityListAPIView.as_view(),name='city-list'),
    path('weather/', CityWeatherAPIView.as_view(),name='city-weather'),
    path('weather/<str:city_name>/',CityWeatherAPIView.as_view(),name='weather-api')
    # path('login/',LoginAPIView.as_view(),name='api-login'),
]
