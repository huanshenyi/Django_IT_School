from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q
from django.views.generic import View
from .forms import LoginForm

#ログインの検証カラムを再度定義
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
             user = UserProfile.objects.get(Q(username=username) | Q(email=username))
             if user.check_password(password):
                 return user
        except Exception as e:
             return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username")
            pass_word = request.POST.get("password")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return render(request, 'index.html', context={"msg": "ユーザー情報確認できません"})
        else:
            return render(request, 'login.html', context={"login_form": login_form})


# class LoginView(View):
#     def get(self, request):
#         return render(request, "login.html")
#
#     def post(self, request):
#         user_name = request.POST.get("username")
#         pass_word = request.POST.get("password")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', context={"msg": "ユーザー情報確認できません"})



# def user_login(request):
#    if request.method == "POST":
#        user_name = request.POST.get("username")
#        pass_word = request.POST.get("password")
#        user = authenticate(username=user_name, password=pass_word)
#        if user is not None:
#            login(request, user)
#            return render(request, 'index.html')
#        else:
#            return render(request, 'login.html', context={"msg": "ユーザー情報確認できません"})
#    elif request.method == "GET":
#        return render(request, "login.html")
