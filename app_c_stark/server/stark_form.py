#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块
from django import forms
# 导入自定义模块

# 设置环境变量


class StarkModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StarkModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
