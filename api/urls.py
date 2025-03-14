from django.urls import path
from api.views import CityListAPIView,CityWeatherAPIView

urlpatterns = [
    path('cities/', CityListAPIView.as_view()),
    path('weather/', CityWeatherAPIView.as_view()),
]
