#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块
from django.urls import path

# 导入自定义模块
from app_c_rbac.views import user_views, theme_views, permissions_views
from app_c_rbac.server import auto
# 设置环境变量

urlpatterns = [
    # 登录、注销、注册
    path('user/login/', user_views.login, name='user_login'),
    path('user/logout/', user_views.logout, name='user_logout'),
    path('user/signup/', user_views.signup, name='user_signup'),
    # 获取图形验证码
    path('user/get_pic_code/<int:pic_width>/<int:pic_height>/<int:text_size>/', user_views.get_pic_code, name='user_get_pic_code'),
    path('user/index/', user_views.index, name='user_index'),
    path('get_menu_data/', theme_views.get_menu_data),
    path('index/', theme_views.index),
    path('menu/permission/allot/', permissions_views.menu_permission_allot),
    path('get_project_all_urls/', auto.get_project_all_urls),
]


