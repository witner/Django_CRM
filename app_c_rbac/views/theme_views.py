#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 第三方模块
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app_c_rbac.models import *


def index(request):
    user_info = request.session.get('user_info')
    user_obj = UserInfo.objects.filter(id=user_info['id']).first()
    print(user_obj)
    return render(request, 'theme/index.html', {'user': user_obj})
    pass

def menu_permission_option(request):
    return render(request, 'rbac/menu_permission.html')


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
            pass
        elif get_type == 'system':
            # 获取系统的所有菜单数据
            menu_queryset = Menu.objects.all()
            menu_node = menu_queryset_to_tree(None, menu_queryset)
        else:
            # 其他
            response_dict.update({
                'error_msg': '无根菜单，请检查数据库'
            })
            pass
        response_dict.update({
            'code': '200',  # 默认200，成功
            'data': {  # 数据
                'node': menu_node,
            }
        })
        print(response_dict)
        return JsonResponse(response_dict)


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
                    'icon': 'glyphicon glyphicon-tags',
                    'children': menu_queryset_to_tree(menu_item, menu_queryset)
                })
            else:
                # 不存在子菜单
                menu_node.append({
                    'id': menu_item.id,
                    'text': menu_item.title,
                    'icon': 'glyphicon glyphicon-tag',
                })
            pass
    else:
        # 没有查询结果
        pass
    print(menu_node)
    return menu_node


