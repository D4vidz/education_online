#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^org_list/', OrganizationView.as_view(), name='org_list'),
    url(r'^add_ask/', AddUserAskView.as_view(), name='add_ask'),
    url(r'^add_fav/', AddFavView.as_view(), name='add_fav'),
    url(r'^home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name='org_courses'),
    url(r'^desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name='org_teacher'),

]
