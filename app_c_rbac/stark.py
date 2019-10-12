#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 导入系统模块
# 第三方模块

# 导入自定义模块
from .models import *
from app_c_stark.server.stark_handler import StarkHandler, get_choice_text
from app_c_stark.server.stark_site import stark_site


# 设置环境变量


class URLHandler(StarkHandler):
    list_display = ['id', 'url', 'name', 'comment', StarkHandler.set_list_display_option_fields]
    pass


class MenuHandler(StarkHandler):
    list_display = ['id', 'title', get_choice_text('类型', 'type'), 'state', 'comment', 'parent_menu', 'app_system',
                    'priority', StarkHandler.set_list_display_option_fields]
    pass


class RoleHandler(StarkHandler):
    list_display = ['id', 'title', 'url_permission', 'menu_permission', StarkHandler.set_list_display_option_fields]


class RoleToUrlPermissionHandler(StarkHandler):
    list_display = ['id', 'role', 'url', StarkHandler.set_list_display_option_fields]


class RoleToMenuPermissionHandler(StarkHandler):
    list_display = ['id', 'role', 'menu', StarkHandler.set_list_display_option_fields]


class UserToRoleHandler(StarkHandler):
    list_display = ['id', 'user', 'role', StarkHandler.set_list_display_option_fields]


class AppSystemHandler(StarkHandler):
    list_display = ['id', 'title', 'comment', StarkHandler.set_list_display_option_fields]


stark_site.register(URL, URLHandler)
stark_site.register(Menu, MenuHandler)
stark_site.register(Role, RoleHandler)
stark_site.register(RoleToUrlPermission, RoleToUrlPermissionHandler)
stark_site.register(RoleToMenuPermission, RoleToMenuPermissionHandler)
stark_site.register(UserToRole, UserToRoleHandler)
stark_site.register(AppSystem, AppSystemHandler)
