#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": '验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': 'error code'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['image']


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']
