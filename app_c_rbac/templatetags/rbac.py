#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块
import re
from django.template import Library
from django.conf import settings
# 导入自定义模块

# 设置环境变量

register = Library()


@register.inclusion_tag('rbac/menu_show_sidebar.html')
def menu_show_sidebar(request):
    """
    菜单展示目录组件
    :param request:
    :return:
    """
    # 第一步：获取当前用户session中保存的菜单权限列表
    menu_permission = request.session.get(settings.MENU_PERMISSION_SESSION_KEY)
    print('----当前用户的菜单权限-----')
    print(menu_permission)
    # 第二步: 返回菜单权限树列表给模板
    return {'menu_node': menu_permission}
