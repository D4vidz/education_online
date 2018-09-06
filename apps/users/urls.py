#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>.*)/', ActivateView.as_view(), name='active'),
    url(r'^forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify/', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^info/', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/', UploadImageView.as_view(), name='image_upload'),
    url(r'^update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    url(r'^sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'^update_email/', UpdateEmailView.as_view(), name='update_email'),
    url(r'^mycourse/', MyCourseView.as_view(), name='mycourse'),
    url(r'^myfav/org/', MyFavOrgView.as_view(), name='myfav_org'),
    url(r'^myfav/teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    url(r'^myfav/course/', MyFavCourseView.as_view(), name='myfav_course'),
    url(r'^my_message/', MyMessageView.as_view(), name='my_message'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),

]
