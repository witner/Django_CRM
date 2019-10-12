#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块

# 导入自定义模块
from app_c_stark.server.stark_handler import StarkHandler, get_choice_text
# 设置环境变量


class SchoolHandler(StarkHandler):
    list_display = ['id', 'title', StarkHandler.set_list_display_option_fields]
