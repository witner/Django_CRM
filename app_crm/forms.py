#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 导入系统模块
import re
# 第三方模块
from django import forms
from django.core.exceptions import ValidationError

# 导入自定义模块
from app_c_rbac.models import UserInfo
# 设置环境变量


class UserInfoFormToSignup(forms.ModelForm):
    """
    用户注册Form
    """
    # 密码确认
    confirm_password = forms.CharField(max_length=128)

    class Meta:
        # 对应model
        model = UserInfo
        # 对应注册字段
        fields = [
            'username',
            'password',
            'email',
            'telephone',
            # 'nickname',
        ]

    def clean_username(self):
        """
        作用：用户注册用户名校验[
            1、校验是否已存在。
        ]
        :return:
        """
        val = self.cleaned_data.get('username')
        if UserInfo.objects.filter(username=val).exists() is False:
            # 不已存在注册的系统账号
            return val
        else:
            raise ValidationError('该系统账号已注册，请使用其它账号注册')

    def clean_telephone(self):
        """
        作用：用户注册手机号校验[
            1、校验是否为手机格式。
            2、校验是否已存在。
        ]
        :return:
        """
        # forms组件局部钩子，校验手机号字段是否满足手机号规范
        val = self.cleaned_data.get('telephone')
        # 校验输入是否满足邮箱格式
        if re.fullmatch(r'(13\d|14[5-9]|15[^4]|16[56]|17[0-8]|18\d|19[189])\d{8}', val):
            if UserInfo.objects.filter(telephone=val).exists() is False:
                # 手机号未注册
                return val
            else:
                raise ValidationError('该手机号已注册，请使用其它手机号注册')
        else:
            raise ValidationError('输入不是正确格式的手机号')

    def clean_email(self):
        """
        作用：用户注册电子邮箱校验[
            1、校验是否为邮箱格式。
            2、校验是否已存在。
        ]
        :return:
        """
        val = self.cleaned_data.get('email')
        # 校验输入是否满足邮箱格式
        if re.fullmatch(r'\w+@\w+\.(com|cn|edu)', val):
            if UserInfo.objects.filter(email=val).exists() is False:
                # 手机号未注册
                return val
            else:
                raise ValidationError('该邮箱已注册，请使用其他邮箱注册')
        else:
            raise ValidationError('输入不是正确格式的邮箱')

    def clean_password(self):
        """
        作用：用户注册密码校验[
            1、校验是否满足密码要求。
        ]
        :return:
        """
        val = self.cleaned_data.get('password')
        if re.fullmatch(r'(?=.*[A-Za-z])(?=.*\d)[a-zA-Z\d]{8,}', val):
            return val
        else:
            raise ValidationError('密码必须至少8个字符，至少1个字母，1个数字')

    def clean(self):
        """
        作用：用户注册确认密码校验[
            1、用于校验两次密码输入是否正确。
        ]
        forms组件全局钩子。
        :return:
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password == confirm_password:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致!')
        else:
            return self.cleaned_data

