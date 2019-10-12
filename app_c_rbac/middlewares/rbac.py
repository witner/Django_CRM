#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    作用：rbac 中间件，用户权限信息校验
    """
    def process_request(self, request):
        """
        作用：[
            1. 获取当前用户请求的URL
            2. 获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
            3. 权限信息匹配
        ]
        :param request:
        :return:
        """

        # 获取当前访问URL
        current_url = request.path_info

        # 检查当前访问URL，是否匹配白名单
        for white_url in settings.WHITE_LIST_URL:
            if re.match(white_url, current_url):
                # 白名单中的URL无需权限验证即可访问
                return None

        # # 获取当前用户session中保存的权限列表，比如['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        # permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        # print(permission_dict)
        # # if not permission_dict:
        # #     return HttpResponse('未获取到用户权限信息，请登录！')
        # #
        # # pass

        # # 获取当前用户session中保存的菜单权限列表
        # menu_permission = request.session.get(settings.MENU_PERMISSION_SESSION_KEY)
        #
        # #
        # if not menu_permission:
        #     return redirect('/app_c_rbac/user/login/')

