import json

from django.shortcuts import render, reverse, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm,\
    UserInfoForm
from users.models import EmailVerifyRecord, Banner
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from course.models import Course
from pure_pagination import PageNotAnInteger, Paginator


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
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'users/index.html', locals())


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
                    return HttpResponseRedirect(reverse('users:index'))
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
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.cleaned_data['email']
            send_register_email(email, 'forget')
            return render(request, 'users/send_success.html')
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


class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'users/usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse(
                '{"status": "success"}', content_type='application/json'
            )
        else:
            return HttpResponse(
                '{"status": "fail"}', content_type='application/json'
            )


class UpdatePwdView(View):

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = modify_form.cleaned_data['pwd1']
            pwd2 = modify_form.cleaned_data['pwd2']
            if pwd1 != pwd2:
                return HttpResponse(
                    '{"status": "fail", "msg": "密码不一致"}', content_type='application/json'
                )
            user = request.user
            user.set_password(pwd2)
            user.save()
            return HttpResponse(
                '{"status": "success"}', content_type='application/json'
            )
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):

    def get(self, request):
        email = request.GET.get('email', '')
        if User.objects.filter(email=email):
            return HttpResponse(
                '{"email": "邮箱已存在"}', content_type='application/json'
            )
        send_register_email(email, 'update_email')
        return HttpResponse(
            '{"status": "success"}', content_type='application/json'
        )


class UpdateEmailView(LoginRequiredMixin, View):

    def post(self, request):

        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "验证码无效"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'users/usercenter-mycourse.html', locals())


class MyFavOrgView(LoginRequiredMixin, View):

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=int(org_id))
            org_list.append(org)
        return render(request, 'users/usercenter-fav-org.html', locals())


class MyFavTeacherView(LoginRequiredMixin, View):

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=int(teacher_id))
            teacher_list.append(teacher)
        return render(request, 'users/usercenter-fav-teacher.html', locals())


class MyFavCourseView(LoginRequiredMixin, View):

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'users/usercenter-fav-course.html', locals())


class MyMessageView(LoginRequiredMixin, View):

    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4, request=request)
        messages = p.page(page)
        return render(request, 'users/usercenter-message.html', locals())


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('users:index'))


def page_not_found(request):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
