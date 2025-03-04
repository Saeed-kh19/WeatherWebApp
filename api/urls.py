from django.urls import path

from api.views import CityListView

urlpatterns = [
    path('cities/',CityListView.as_view()),
]
