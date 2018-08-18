from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from .models import EmailVerifyRecord
from utils.email_send import send_register_email


User = get_user_model()


# 邮箱和用户名都能登录
class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):

    def get(self, request):
        return render(request, 'users/index.html')


class LoginView(View):

    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'users/index.html')
                else:
                    return render(request, 'users/login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
            else:
                return render(request, 'users/login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'users/register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['email']
            if User.objects.filter(email=username):
                return render(request, 'users/register.html', {'register_form': register_form, 'msg': '用户已存在'})
            password = register_form.cleaned_data['password']
            user = User(username=username, email=username, is_active=False)
            user.set_password(password)
            user.save()
            send_register_email(username, 'register')
            return render(request, 'users/login.html')
        else:
            return render(request, 'users/register.html', {'register_form': register_form})


class ActivateView(View):

    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                email = record.email
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'users/active_fail.html')
        return render(request, 'users/login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'users/forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm()
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            send_register_email(email, 'forget')
        else:
            return render(request, 'users/forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'users/password_reset.html', {'email': email})
            else:
                return render(request, 'users/active_fail.html')
        return render(request, 'users/login.html')


class ModifyPwdView(View):

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = modify_form.cleaned_data['password1']
            pwd2 = modify_form.cleaned_data['password2']
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'users/password_reset.html', {'email': email, 'msg': '两次密码不一致'})
            user = User.objects.get(email=email)
            user.set_password(pwd2)
            user.save()

            return render(request, 'users/login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'users/password_reset.html', {'email': email, 'modify_form': modify_form})
