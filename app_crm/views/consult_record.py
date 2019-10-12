#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块
from django.utils.safestring import mark_safe
from django.urls import reverse
# 导入自定义模块
from app_c_stark.server.stark_handler import StarkHandler, get_choice_text
# 设置环境变量


class ConsultRecordHandler(StarkHandler):
    # model_form_class = PrivateCustomerModelForm


    list_display = ['customer', 'consultant', 'note', 'date', StarkHandler.set_list_display_option_fields]

