#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 第三方模块
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.template import Library
from app_c_rbac.models import *


def menu_permission_allot(request):
    """
    作用：菜单权限分配页面
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'rbac/menu_permission_allot.html')
    elif request.method == 'POST':
        pass
    else:
        pass


def menu_permission_get(current_user):
    """
    作用：根据登录用户获取菜单权限树，并返回
    :param current_user: 当前登录用户
    :return: 菜单权限树列表
    """
    # 第一步：获取当前用户
    # 第二步：根据用户查询对应菜单权限的id
    t = current_user.role.filter(menu_permission__isnull=False).values("menu_permission__id").distinct()
    # 第三步：根据第一步查询结果，查询对应menu_queryset
    menu_queryset = Menu.objects.filter(id__in=t).filter(type__in=[1, 2])
    # 第四步：生成菜单树列表
    menu_node = menu_queryset_to_tree(None, menu_queryset)
    # 第五步：返回菜单树列表结果
    print('##菜单权限', menu_node)
    return menu_node


def get_menu_data(request):
    """
    作用：从数据库获取菜单数据，返回json给前端
    :param request:
    :return:
    """
    if request.method == 'GET':
        response_dict = {
            'code': '400',  # 默认200，成功
            'data': {  # 数据
            },
            'error_msg': None
        }
        get_type = request.GET.get('get_type', 'personal')
        menu_node = []

        if get_type == 'personal':
            # 获取个人的菜单数据

            # 第一步：获取当前用户
            user_obj = request.user
            # 第二步：根据用户查询对应菜单权限的id
            t = user_obj.role.filter(menu_permission__isnull=False).values("menu_permission__id").distinct()
            # 第三步：根据第一步查询结果，查询对应menu_queryset
            menu_queryset = Menu.objects.filter(id__in=t).filter(type__in=[1, 2])
            # 第四步：生成菜单树列表
            menu_node = menu_queryset_to_tree(None, menu_queryset)
            # 第五步：返回菜单树列表结果
            return menu_node

        elif get_type == 'system':
            # 获取系统的所有菜单数据，以JSON数据返回
            menu_queryset = Menu.objects.all()
            menu_node = menu_queryset_to_tree(None, menu_queryset)
            response_dict.update({
                'code': '200',  # 默认200，成功
                'data': {  # 数据
                    'node': menu_node,
                }
            })
            # print(response_dict)
            return JsonResponse(response_dict)
        else:
            # 其他
            response_dict.update({
                'error_msg': '无根菜单，请检查数据库'
            })
            pass


def menu_queryset_to_tree(parent_menu, menu_queryset):
    """
    作用: 将menu_queryset对象转换成功树形结构的list
    :param parent_menu: 根菜单
    :param menu_queryset: 菜单查询集
    :return: menu_node，树形结构列表
    """
    menu_node = []
    root_menu_queryset = menu_queryset.filter(parent_menu=parent_menu)
    if root_menu_queryset.exists():
        # 存在查询结果
        for menu_item in root_menu_queryset:
            r = menu_queryset_to_tree(menu_item, menu_queryset)
            if r:
                menu_node.append({
                    'id': menu_item.id,
                    'text': menu_item.title,
                    'icon': menu_item.icon,
                    'url': '#' if menu_item.url is None else menu_item.url.url,
                    'children': menu_queryset_to_tree(menu_item, menu_queryset)
                })
            else:
                # 不存在子菜单
                menu_node.append({
                    'id': menu_item.id,
                    'text': menu_item.title,
                    'icon': menu_item.icon,
                    'url': '#' if menu_item.url is None else menu_item.url.url,
                })
            pass
    else:
        # 没有查询结果
        pass
    return menu_node
