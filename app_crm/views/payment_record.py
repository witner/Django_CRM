#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块

# 导入自定义模块
from app_c_stark.server.stark_handler import StarkHandler, get_choice_text
# 设置环境变量


class PaymentRecordHandler(StarkHandler):
    list_display = ['customer', 'consultant', get_choice_text('缴费类型', 'pay_type'), 'paid_fee', 'class_list',
                    StarkHandler.set_list_display_option_fields]
