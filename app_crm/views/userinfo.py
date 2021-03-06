#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块
from io import BytesIO
import random
import re
import os
# 第三方模块
from django.urls import path
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from app_c_stark.server.stark_handler import StarkHandler, get_choice_text
from ..models import *
from ..forms import UserInfoFormToSignup
from django.conf import settings
from app_c_rbac.views import permissions_views

from PIL import Image, ImageDraw, ImageFont

# 导入自定义模块
# 设置环境变量


class UserInfoHandler(StarkHandler):

    list_display = ['nickname', get_choice_text('性别', 'sex'),'username', 'telephone', 'email', 'depart', StarkHandler.set_list_display_option_fields]

    def extend_urlpatterns(self):
        """
        作用：用于添加其他url，当默认url（增删改查）不满足时使用
        :return: 列表，默认空列表
        """
        urlpatterns = [
            # 登录、注销、注册
            path('login/', self.login, name=self.get_url_name('login')),
            path('logout/', self.logout, name=self.get_url_name('logout')),
            path('signup/', self.signup, name=self.get_url_name('signup')),
            # 获取图形验证码
            path('get_pic_code/<int:pic_width>/<int:pic_height>/<int:text_size>/', self.get_pic_code,
                 name=self.get_url_name('get_pic_code')),
        ]
        return urlpatterns

    # 函数方法
    def login(self, request):
        """
        作用：登录校验
        :param request:
        :return: JSON数据
        """
        if request.method == "GET":
            return render(request, 'userinfo/login.html')
        elif request.method == "POST":
            # POST请求
            response_json = {
                'code': '400',  # 默认200，成功
                'msg': '',  # 消息内容
                'data': {  # 数据
                }
            }

            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            pic_code = request.POST.get('pic_code', None)

            if pic_code:
                if pic_code == request.session['str_pic_code']:
                    # 如果图形验证码正确，校验用户名密码

                    if username and password:
                        # 如果验证成功返回对象，否则返回None
                        # 检查输入用户名是否匹配邮箱，或者手机号
                        if re.fullmatch(r'\w+@\w+\.(com|cn|edu)', username):
                            # 匹配邮箱
                            res = UserInfo.objects.filter(email=username)
                        elif re.fullmatch(r'(13\d|14[5-9]|15[^4]|16[56]|17[0-8]|18\d|19[189])\d{8}', username):
                            # 匹配手机号
                            res = UserInfo.objects.filter(telephone=username)
                        else:
                            # 匹配系统账号
                            res = UserInfo.objects.filter(username=username)

                        if res.exists():
                            # 查询结果存在，校验密码是否正常
                            obj_user = res.first()
                            print(obj_user.password, password)
                            if obj_user.password != password:
                            # if obj_user.check_password(password) is False:
                                # 密码校验失败
                                response_json.update({
                                    'msg': '输入邮箱地址、手机号或系统账号，密码错误',
                                    'data': {
                                        'field': 'username',
                                    }
                                })
                            else:
                                # 密码校验通过，session创建，request.user = user 对象产生，保存session对象，避免下次登录
                                # auth.login(request, obj_user)
                                request.session['user_info'] = {'id': obj_user.id, 'nickname': obj_user.nickname}

                                # 获取用户对应菜单权限, 并保存在session中
                                request.session[
                                    settings.MENU_PERMISSION_SESSION_KEY] = permissions_views.menu_permission_get(
                                    obj_user)

                                response_json.update({
                                    'code': '200',  # 默认200，成功
                                    'msg': '登录成功',
                                })
                        else:
                            # 查询没有结果，表示用户不存在
                            response_json.update({
                                'msg': '输入邮箱地址、手机号或系统账号，密码错误',
                                'data': {
                                    'field': 'username',
                                }
                            })
                    else:
                        response_json.update({
                            'msg': '输入邮箱地址、手机号或系统账号，密码不能为空',
                            'data': {
                                'field': 'username',
                            }
                        })
                else:
                    response_json.update({
                        'msg': '输入验证码不正确',
                        'data': {
                            'field': 'pic_code',
                        }
                    })
            else:
                response_json.update({
                    'msg': '输入形验证码不能为空',
                    'data': {
                        'field': 'pic_code',
                    }
                })
            return JsonResponse(response_json)
        else:
            pass

    def logout(self, request):
        """
        用户注销操作
        :param request:
        :return:
        """
        auth.logout(request)
        return redirect(self.get_url_name('login'))

    def signup(self, request):
        """
        用户注册操作
        :param request:
        :return:
        """
        if request.method == 'GET':
            # get 请求
            return render(request, 'userinfo/signup.html')

        elif request.method == 'POST':
            response_dict = {
                'code': '400',  # 默认200，成功
                'msg': '',  # 消息内容
                'data': {  # 数据
                }
            }

            form = UserInfoFormToSignup(request.POST)
            if form.is_valid():
                pass
                obj_user = UserInfo.objects.create(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    telephone=form.cleaned_data['telephone'],
                    email=form.cleaned_data['email']
                )
                if obj_user:
                    response_dict.update({
                        'code': '200',
                        'msg': '注册成功',
                        'data': {
                            'username': form.cleaned_data['username'],
                        }
                    })
                    return JsonResponse(response_dict)
                else:
                    return JsonResponse(response_dict)
            else:
                response_dict.update({
                    'msg': '注册失败，输入字段错误',
                    'data': {
                        'username': form.errors.get("username", None),
                        'email': form.errors.get("email", None),
                        'telephone': form.errors.get("telephone", None),
                        'password': form.errors.get("password", None),
                        'confirm_password': form.errors.get("__all__", None),
                    }
                })
            return JsonResponse(response_dict)
        else:
            pass

    def get_pic_code(self, request, pic_width=150, pic_height=26, text_num=4, text_size=20):
        """
        登录验证码
        :param request:
        :param pic_width: 图片宽度
        :param pic_height: 图片高度
        :param text_num: 验证码字符个数
        :param text_size: 验证码字符大小
        :return:
        """
        img = Image.new('RGB', (pic_width, pic_height), color='white')
        draw = ImageDraw.Draw(img)
        # ttf_file_path = os.path.join(settings.BASE_DIR, 'app_c_rbac/static/ttf/经典行书简.TTF'),
        font = ImageFont.truetype(os.path.join(settings.BASE_DIR, 'app_c_rbac/static/ttf/经典行书简.TTF'), size=text_size)

        f = BytesIO()

        # 生成验证码
        str_pic_code = ''
        for i in range(text_num):
            # 随机数
            num = random.randint(0, 9)
            lowercase = chr(random.randint(97, 122))  # 取小写字母
            uppercase = chr(random.randint(65, 90))  # 取大写字母
            character = str(random.choice([num, lowercase, uppercase]))  # 从数字，小写字母，大写字母随机选择一个

            x = random.randint(i * int(pic_width / text_num), (i + 1) * int(pic_width / text_num) - text_size)
            y = random.randint(0, int(pic_height - text_size))
            # print(i)
            str_pic_code += character
            draw.text((x, y), character, 'black', font=font)

            # 生成干扰线
            x1 = random.randint(0, pic_width)
            x2 = random.randint(0, pic_width)
            y1 = random.randint(0, pic_height)
            y2 = random.randint(0, pic_height)
            draw.line((x1, y1, x2, y2), fill='black')

        img.save(f, 'png')
        data = f.getvalue()
        # 验证码用session保存
        request.session['str_pic_code'] = str_pic_code

        return HttpResponse(data)
