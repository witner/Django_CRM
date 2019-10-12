#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块
from django.utils.safestring import mark_safe
from django.urls import reverse
# 导入自定义模块
from app_c_stark.server.stark_handler import StarkHandler, get_choice_text
# 设置环境变量


class ClassListHandler(StarkHandler):

    def display_course(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '班级'
        return "%s %s期" % (obj.course.name, obj.semester,)

    def display_course_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '上课记录'
        # record_url = reverse('stark:app_crm_courserecord_list', kwargs={'class_id': obj.pk})
        return mark_safe('<a target="_blank" href="#">上课记录</a>')

    list_display = [
        'school',
        display_course,
        'price',
        'start_date',
        'class_teacher',
        'tech_teachers',
        display_course_record,
        StarkHandler.set_list_display_option_fields
    ]

