"""education_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from django.views.static import serve
from education_online.settings import MEDIA_ROOT

import xadmin

urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'', include('users.urls', namespace='users')),
    url(r'', include('organization.urls', namespace='organization')),
    url(r'', include('operation.urls', namespace='operation')),
    url(r'', include('course.urls', namespace='course')),

    url(r'^captcha/', include('captcha.urls')),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]

# 404
handler404 = 'users.views.page_not_found'
# 500
handler500 = 'users.views.page_error'
