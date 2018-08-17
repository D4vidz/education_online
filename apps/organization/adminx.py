#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .models import *


class CityDictAdmin(object):
    """城市"""

    list_display = ['name', 'desc', 'c_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'c_time']


class CourseOrgAdmin(object):
    """机构"""

    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'c_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'city__name', 'address', 'c_time']


class TeacherAdmin(object):
    """老师"""

    list_display = ['name', 'org', 'work_years', 'work_company', 'c_time']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'click_nums', 'fav_nums', 'c_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
