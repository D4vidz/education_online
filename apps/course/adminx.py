#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xadmin

from .models import *


class CourseAdmin(object):
    """课程"""

    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']


class LessonAdmin(object):
    """章节"""

    list_display = ['course', 'name', 'c_time']
    search_fields = ['course', 'name']
    # 这里course__name是根据课程名称过滤
    list_filter = ['course__name', 'name', 'c_time']


class VideoAdmin(object):
    """视频"""

    list_display = ['lesson', 'name', 'c_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'c_time']


class CourseResourceAdmin(object):
    """课程资源"""

    list_display = ['course', 'name', 'download', 'c_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'c_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(Lesson, LessonAdmin)
