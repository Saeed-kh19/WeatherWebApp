# # from django.shortcuts import render, redirect
# # from pyexpat.errors import messages
# # from django.contrib.auth.models import User
# #
# #
# # def login_view(request):
# #     if request.method == "POST":
# #         username = request.POST.get("username")
# #         email = request.POST.get("email")
# #
# #         try:
# #             user = User.objects.get(username=username,email_address=email)
# #             request.session['user_id'] = user.id
# #             return redirect('home')
# #         except User.DoesNotExist:
# #             messages.error(request, 'Username not found!')
# #
# #     return render(request,'index.html')
# #
# # def home_view(request):
# #     user_id = request.session.get('user_id')
# #     if not user_id:
# #         return redirect('login')
# #
# #     user = User.objects.get(id=user_id)
# #     return render(request,'index.html',{'user':user})
# #
# # def logout_view(request):
# #     request.session.flush()
# #     return redirect('login')
# from django.contrib.auth.models import User
# from django.shortcuts import render
# from django.views import View
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
#
# class LoginView(View):
#     def post(self,request,*args,**kwargs):
#         username = request.data.get("username")
#         email = request.data.get("email")
#
#         if not username or not email:
#             return Response({'Error': 'username and email is required!'}, status=400)
#         try:
#             user = User.objects.get(username__iexact=username,email__iexact=email)
#             if Token.objects.filter(user=user).exists():
#                 token = Token.objects.get(user=user)
#             else:
#                 token = Token.objects.create(user=user)
#             return Response({'token': token.key})
#         except User.DoesNotExist:
#             return Response({'Error': 'username or email is invalid!'}, status=400)
#     def get(self,request,*args,**kwargs):
#         return render(request,'index.html')

# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from django.shortcuts import render
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator


from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for POST requests
class LoginView(View):
    def get(self, request, *args, **kwargs):
        # Render the login page
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        # Handle login logic and token generation
        username = request.POST.get("username")
        email = request.POST.get("email")

        if not username or not email:
            return JsonResponse({'Error': 'username and email is required!'}, status=400)

        try:
            # Case-insensitive username and email lookup
            user = User.objects.get(username__iexact=username, email__iexact=email)
            # Retrieve or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'Error': 'username or email is invalid!'}, status=404)
