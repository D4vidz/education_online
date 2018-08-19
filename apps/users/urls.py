#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from users.views import LoginView, IndexView, RegisterView, ActivateView, ForgetPwdView, ResetView
from users.views import ModifyPwdView


urlpatterns = (
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>.*)/', ActivateView.as_view(), name='active'),
    url(r'^forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify/', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^$', IndexView.as_view(), name='index'),
)
