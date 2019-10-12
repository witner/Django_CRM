#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块
from collections import OrderedDict
# 第三方模块
from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import URLPattern, URLResolver
# 导入自定义模块

# 设置环境变量


"""
URLPattern : 代表具有路由分发的路由，比如：path('admin/', admin.site.urls), 其包含多个 URLResolver
URLResolver ：代表调用对应函数的路由，比如：path('user/login/', user_views.login, name='user_login'),
"""


def recursion_url(urlpatterns, urlresolver_namespace, urlresolver_base, urlpatterns_dict):
    """
    作用：递归获取url直到URLPattern
    :param pre_namespace: namespace前缀，以后用户拼接name
    :param pre_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for url_obj in urlpatterns:
        if isinstance(url_obj, URLPattern):
            # 表示当前url对象为URLPattern，为非路由分发

            if urlresolver_namespace:
                # 如果当前url所属路由分发，存在命名空间
                # 当前url的反向解析名称为 namespace:name
                urlpattern_name = '%s:%s' % (urlresolver_namespace, url_obj.name)
            else:
                # 如果当前url所属路由分发，没有命名空间.当前url的反向解析名称为 name
                urlpattern_name = url_obj.name

            urlpattern_base = urlresolver_base + url_obj.pattern._route

            # 将该url，添加的urlpatterns_dict
            urlpatterns_dict[urlpattern_name] = {'name': urlpattern_name, 'url_base': urlpattern_base}
            pass
        elif isinstance(url_obj, URLResolver):
            pass
        else:
            pass
        print(urlpatterns_dict)

    pass


def get_project_all_urls(request):
    """
    作用：获取项目中所有使用的url
    :param request:
    :return:
    """

    project_urlpatterns_dict = OrderedDict()
    # 根据项目setting中的 ROOT_URLCONF 配置导入
    md = import_string(settings.ROOT_URLCONF)
    # print(md.urlpatterns)
    recursion_url(urlpatterns=md.urlpatterns, urlresolver_namespace=None, urlresolver_base='/',
                  urlpatterns_dict=project_urlpatterns_dict)
    print(project_urlpatterns_dict)
    return HttpResponse('OK')
    pass
