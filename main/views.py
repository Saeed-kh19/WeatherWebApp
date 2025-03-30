# from django.contrib.auth.models import User
# from django.shortcuts import render
# from rest_framework.authtoken.models import Token
# from django.http import JsonResponse
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
#
# @method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for POST requests
# class LoginView(View):
#     def get(self, request, *args, **kwargs):
#         # Render the login page (always accessible)
#         return render(request, 'index.html')
#
#     def post(self, request, *args, **kwargs):
#         # Handle login logic and token generation
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#
#         if not username or not email:
#             return JsonResponse({'Error': 'username and email are required!'}, status=400)
#
#         try:
#             user = User.objects.get(username__iexact=username, email__iexact=email)
#             token, created = Token.objects.get_or_create(user=user)
#             return JsonResponse({'token': token.key}, status=200)
#         except User.DoesNotExist:
#             return JsonResponse({'Error': 'username or email is invalid!'}, status=404)
#
# class HomeView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'home.html')

from django.shortcuts import render
from django.views import View
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


@method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for POST requests
class LoginView(View):
    def get(self, request, *args, **kwargs):
        # Render the login page (always accessible)
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        # Handle login logic and token generation
        username = request.POST.get("username")
        email = request.POST.get("email")

        if not username or not email:
            return JsonResponse({'Error': 'username and email are required!'}, status=400)

        try:
            user = User.objects.get(username__iexact=username, email__iexact=email)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'Error': 'username or email is invalid!'}, status=404)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        # Render the home page
        return render(request, 'home.html')

