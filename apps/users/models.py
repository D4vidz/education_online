from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    gender_choices = (
        ('male', '男'),
        ('female', '女')
    )

    nick_name = models.CharField(verbose_name='昵称', max_length=50, default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', max_length=10, choices=gender_choices, default='男')
    address = models.CharField(verbose_name='地址', max_length=128, blank=True, null=True)
    mobile = models.CharField(verbose_name='电话', max_length=11, blank=True, null=True)
    image = models.ImageField(verbose_name='头像', upload_to='users/image/%Y%m', default='users/image/default.png', max_length=100)

    class Meta:
        db_table = 't_user_profile'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    send_choices = (
        ('register', '注册'),
        ('forget', '找回密码')
    )

    code = models.CharField(verbose_name='验证码', max_length=20)
    email = models.EmailField(verbose_name='邮箱', max_length=50)
    send_type = models.CharField(verbose_name='类型', choices=send_choices, max_length=10)
    c_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        db_table = 't_email_record'
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.send_type + '--->' + self.email


class Banner(models.Model):
    title = models.CharField(verbose_name='标题', max_length=100)
    image = models.ImageField(verbose_name='轮播图', upload_to='users/banner/%Y%m', max_length=100)
    url = models.URLField(verbose_name='访问地址', max_length=200)
    index = models.IntegerField(verbose_name='顺序', default=100)
    c_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
