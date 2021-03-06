# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-19 08:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(max_length=200, verbose_name='评论')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '课程评论',
                'verbose_name_plural': '课程评论',
                'db_table': 't_course_comment',
            },
        ),
        migrations.CreateModel(
            name='UserAsk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机')),
                ('course_name', models.CharField(max_length=50, verbose_name='课程名')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户咨询',
                'verbose_name_plural': '用户咨询',
                'db_table': 't_user_ask',
            },
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户课程',
                'verbose_name_plural': '用户课程',
                'db_table': 't_user_course',
            },
        ),
        migrations.CreateModel(
            name='UserFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_id', models.IntegerField(default=0, verbose_name='数据id')),
                ('fav_type', models.IntegerField(choices=[(1, '课程'), (2, '课程机构'), (3, '讲师')], default=1, verbose_name='收藏类型')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户收藏',
                'verbose_name_plural': '用户收藏',
                'db_table': 't_user_favorite',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=0, verbose_name='接受用户')),
                ('message', models.CharField(max_length=500, verbose_name='消息内容')),
                ('has_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '用户消息',
                'verbose_name_plural': '用户消息',
                'db_table': 't_user_message',
            },
        ),
    ]
