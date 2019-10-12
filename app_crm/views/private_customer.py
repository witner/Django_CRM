#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块
from django.utils.safestring import mark_safe
from django.urls import reverse
# 导入自定义模块
from app_c_stark.server.stark_handler import StarkHandler, get_choice_text
# 设置环境变量


class PrivateCustomerHandler(StarkHandler):
    # model_form_class = PrivateCustomerModelForm

    def display_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '跟进'
        # record_url = reverse('stark:web_consultrecord_list', kwargs={'customer_id': obj.pk})
        return mark_safe('<a target="_blank" href="#">跟进</a>')

    def display_pay_record(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '缴费'
        # record_url = reverse('stark:web_paymentrecord_list', kwargs={'customer_id': obj.pk})
        return mark_safe('<a target="_blank" href="#">缴费</a>')

    list_display = ['name', 'qq', 'course',
                    get_choice_text('状态', 'status'), display_record, display_pay_record, StarkHandler.set_list_display_option_fields]

