from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic import View
from .forms import LoginForm, RegisterForm,ForgetForm,ModifyPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from django.http import HttpResponse

#ログインの検証カラムを再度定義
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
             user = UserProfile.objects.get(Q(username=username) | Q(email=username))
             if user.check_password(password):
                 return user
        except Exception as e:
             return None

#ログイン
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
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', context={"msg": "アクティブユーザーではない"})
            else:
                return render(request, 'login.html', context={"msg": "ユーザー情報確認できません"})
        else:
            return render(request, 'login.html', context={"login_form": login_form})



class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return HttpResponse('無効なリンクです')
        return render(request, 'login.html')


#新規登録
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', context={'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email")
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html',
                              context={'register_form': register_form, 'msg': 'email既に使われている'})
            pass_word = request.POST.get("password")
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(email, "register")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', context={'register_form': register_form})

class ForgetPwdVied(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', context={'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            send_register_email(email, "forget")
            return HttpResponse("メール送信しました")
        else:
            return render(request, 'forgetpwd.html', context={'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', context={'email': email})
        else:
            return HttpResponse('無効なリンクです')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            email = request.POST.get('email')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html',
                              context={'email': email, 'msg': '二回の入力一致しません'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email')
            return render(request, 'password_reset.html',
                          context={'email': email, 'modify_form': modify_form})








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
