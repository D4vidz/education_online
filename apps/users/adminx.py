#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xadmin

from .models import *
from xadmin import views


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'c_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'c_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'c_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'c_time']


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '在线教育'
    site_footer = 'ZZY'
    menu_style = 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
