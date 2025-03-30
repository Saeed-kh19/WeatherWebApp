from django.contrib import admin
from django.urls import path, include

from main.views import LoginView, HomeView

# from api.views import login_view

# from main.views import login_view, home_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
    # path('login/', LoginView.as_view(), name='login-page'),
    path('login/', LoginView.as_view(), name='login'),
    # path('home/', HomeView.as_view(), name='home-page'),
    path('home/', HomeView.as_view(), name='home'),
    # path('home/',home_view,name='home'),
    # path('logout/',logout_view,name='logout'),
]
