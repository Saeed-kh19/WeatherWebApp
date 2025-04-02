from django.shortcuts import render
from django.views import View
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
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
        return render(request, 'home.html')
