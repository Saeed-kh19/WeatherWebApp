from django.urls import path

from api.views import CityListView, CityWeatherView

urlpatterns = [
    path('cities/',CityListView.as_view()),
    path('weather/',CityWeatherView.as_view()),
]
