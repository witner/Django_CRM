#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块
from types import FunctionType
# 第三方模块
from django.urls import re_path, reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render, HttpResponse, redirect

# 导入自定义模块
from app_c_stark.utils.pagination import Pagination
from app_c_stark.server.stark_form import StarkModelForm


# 设置环境变量

#
# 导入自定义模块


def get_choice_text(title, field):
    """
    作用：
    :param title: 希望页面显示的标题
    :param field: 数据库字段
    :return: inner方法
    """

    # inner为闭包函数，作用执行
    def inner(self, obj=None, is_header=True):
        if is_header:
            return title
        else:
            # str_method 为拼接后的函数方法，用于执行获取对应Model类中字段对应的CHOICES
            str_method = 'get_%s_display' % field
            return getattr(obj, str_method)()

    return inner


# 类
class StarkHandler(object):
    """
    StarkHandler:类，负责增删改查操作
    """
    pass

    # 列表显示字段
    list_display = []

    def __init__(self, stark_site_obj, model_class, prev):
        """
        初始化方法，
        :param stark_site_obj: StarkSite类实例化的对象
        :param model_class: 模型类
        """
        self.stark_site_obj = stark_site_obj
        self.model_class = model_class
        self.model_form_class = None
        self.prev = prev
        self.delete_template = None

    def get_urlpatterns(self):
        """
        根据模型中定义的model类，自动生成对应的增删改查url路由。
        比如：模型类为app_01.UserInfo，那么自动生成路由[
            /stark/app_01/userinfo/add/,
            /stark/app_01/userinfo/delete/(\d+)/,
            /stark/app_01/userinfo/modify/(\d+)/,
            /stark/app_01/userinfo/detail/(\d+)/,
            /stark/app_01/userinfo/list/,
        ]
        :return: 返回urlpatterns
        """
        # 初始化默认url
        urlpatterns = [
            re_path(r'^add/$', self.add_view, name=self.get_url_name('add')),
            re_path(r'^delete/(?P<pk>\d+)/$', self.delete_view, name=self.get_url_name('delete')),
            re_path(r'^modify/(?P<pk>\d+)/$', self.modify_view, name=self.get_url_name('modify')),
            re_path(r'^detail/(?P<pk>\d+)/$', self.detail_view, name=self.get_url_name('detail')),
            re_path(r'^list/$', self.list_view, name=self.get_url_name('list')),
        ]
        # 初始化自定义扩展url
        urlpatterns.extend(self.extend_urlpatterns())
        # 返回
        return urlpatterns

    def extend_urlpatterns(self):
        """
        作用：用于添加其他url，当默认url（增删改查）不满足时使用
        :return: 列表，默认空列表
        """
        return []

    def get_url_name(self, param):
        """
        作用：生成urls的反射name
        :param param: 参数
        :return:name
        """
        # 获取对应模型的所在app名称，和模型类的名称

        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            name = '%s_%s_%s_%s' % (app_label, model_name, self.prev, param)
        else:
            name = '%s_%s_%s' % (app_label, model_name, param)
        return name

    def get_url_reverse(self, url_name, is_param=False, param=None):
        """
        作用：根据url名称获得对应url
        :param url_name: url名称
        :return:name
        """
        # 获取对应模型的所在app名称，和模型类的名称
        if is_param:
            url_base = reverse("%s:%s" % (self.stark_site_obj.namespace, url_name), args=param)
        else:
            url_base = reverse("%s:%s" % (self.stark_site_obj.namespace, url_name))
        return url_base

    # 第二部分，添加默认增删改查方法
    def add_view(self, request, *args, **kwargs):
        """
        记录增加
        :param request:
        :return:
        """
        model_form_class = self.get_model_form_class(True, request, None, *args, **kwargs)
        if request.method == 'GET':
            form = model_form_class()
            return render(request, 'add_view.html', {'form': form})
        elif request.method == 'POST':
            form = model_form_class(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_url_reverse(self.get_url_name('list')))
            pass
        else:
            pass

    def delete_view(self, request, pk):
        """
        记录删除
        :param request:
        :param pk: 主键
        :return:
        """
        origin_list_url = self.get_url_reverse(self.get_url_name('list'))
        if request.method == 'GET':
            return render(request, self.delete_template or 'delete_view.html', {'cancel': origin_list_url})
        elif request.method == 'POST':
            response = self.model_class.objects.filter(pk=pk).delete()
            return redirect(origin_list_url)
        else:
            pass

    def modify_view(self, request, pk, *args, **kwargs):
        """
        记录修改
        :param request:
        :param pk: 主键
        :return:
        """
        modify_obj = self.model_class.objects.filter(pk=pk).first()
        if not modify_obj:
            return HttpResponse('要修改的数据不存在，请重新选择！')

        model_form_class = self.get_model_form_class(False, request, None, *args, **kwargs)
        if request.method == 'GET':
            form = model_form_class(instance=modify_obj)
            return render(request, 'modify_view.html', {'form': form})
        elif request.method == 'POST':
            form = model_form_class(data=request.POST, instance=modify_obj)
            if form.is_valid():
                form.save()
                return redirect(self.get_url_reverse(self.get_url_name('list')))
            pass
        else:
            pass

    def detail_view(self, request, pk):
        """
        记录详情
        :param request:
        :param pk: 主键
        :return:
        """
        pass
        return HttpResponse('详情页面')

    def list_view(self, request):
        """
        记录列表
        :param request:
        :return:
        """
        # 查询符合条件的列表数据，
        data_queryset = self.model_class.objects.all()

        # 添加按钮设置
        add_btn = '<a class="btn btn-primary" href="%s" role="button">添加</a>' \
                  % self.get_url_reverse(self.get_url_name('add'))

        # 分页效果设置
        page = int(request.GET.get('page', 1))  # 请求的当前页码，默认为第一页
        url_base = request.path_info  # 请求的url基础
        url_params = request.GET.copy()  # 请求的url参数，需要copy保存，_mutable设置为True方可修改url_params
        url_params._mutable = True
        data_count = data_queryset.count()  # 查询数据的总数
        entries = int(request.GET.get('entries', 10))  # 请求的每页显示条目数量

        pager_obj = Pagination(page=page, url_base=url_base, url_params=url_params, data_count=data_count,
                               entries=entries)

        # 第一步：加载列表需要显示的字段信息
        list_display = self.set_list_display()

        # 第二步：页处理面要显示的列表头部
        table_header_list = []
        for key_or_func in list_display:
            if isinstance(key_or_func, FunctionType):
                # key_or_func是函数
                verbose_name = key_or_func(self, obj=None, is_header=True)
            else:
                # key_or_func是字段
                verbose_name = self.model_class._meta.get_field(key_or_func).verbose_name
            table_header_list.append(verbose_name)

        # 处理页面列表的内容数据
        """
        数据格式 [
            ['id',  'username']
        ]
        """
        table_body_list = []
        data_queryset = data_queryset[pager_obj.data_index_start:pager_obj.data_index_end]
        for data_obj in data_queryset:
            row = []
            for key_or_func in list_display:
                if isinstance(key_or_func, FunctionType):
                    # key_or_func是函数
                    row.append(key_or_func(self, obj=data_obj, is_header=False))
                else:
                    # key_or_func是字段
                    row.append(getattr(data_obj, key_or_func))
            table_body_list.append(row)

        response = {
            'table_options': add_btn,
            'table_header_list': table_header_list,
            'table_body_list': table_body_list,
            'table_page': pager_obj.get_page_html(),
        }
        print(response)
        return render(request, 'list_view.html', {'response': response})

    # list_view扩展方法
    def set_list_display(self):
        """
        自定义，设置页面上应该显示的列表，默认为self.list_display
        :return:
        """
        value = []
        value.extend(self.list_display)
        return value

    def set_list_display_option_fields(self, obj=None, is_header=True):
        """
        作用：设置列表显示的扩展字段，比如操作（默认：编辑、删除、详情）
        :return:
        """
        if is_header:
            return "操作"

        modify = '<a class="btn btn-default" href="%s" role="button">编辑</a>' \
                 % self.get_url_reverse(self.get_url_name('modify'), is_param=True, param=(obj.pk,))
        delete = '<a class="btn btn-default" href="%s" role="button">删除</a>' \
                 % self.get_url_reverse(self.get_url_name('delete'), is_param=True, param=(obj.pk,))
        detail = '<a class="btn btn-default" href="%s" role="button">详情</a>' \
                 % self.get_url_reverse(self.get_url_name('detail'), is_param=True, param=(obj.pk,))

        option = modify + delete + detail

        return mark_safe(option)

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        if self.model_form_class:
            return self.model_form_class

        class DynamicModelForm(StarkModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm
