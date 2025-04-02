from django.contrib import admin
from django.urls import path, include

from main.views import LoginView, HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
]