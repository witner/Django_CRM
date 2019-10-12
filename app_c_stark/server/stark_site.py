#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入系统模块

# 第三方模块
from django.urls import re_path
# 导入自定义模块
from app_c_stark.server.stark_handler import StarkHandler

# 设置环境变量


class StarkSite(object):
    """
    作用：用户快速生成对应url路由，和方法
    """
    pass

    def __init__(self):

        self.registration_list = []         # 注册列表
        self.app_name = 'stark'             # app名称
        self.namespace = 'stark'            # 名称空间，用户路由反向生成URL

    def register(self, model_class, handler_class=None, prev=None):
        """
        作用：对外注册入口，提供模型类，自动生成对应url
        :param model_class: 是models中的数据库表对应的类。 models.UserInfo
        :param handler_class: 处理请求的视图函数所在的类
        :return: None
        实例
        self.registration_list = [
            {'model_class':models.Depart,'handler': DepartHandler(models.Depart,prev)对象中有一个model_class=models.Depart   },
            {'model_class':models.UserInfo,'handler':  StarkHandler(models.UserInfo,prev)对象中有一个model_class=models.UserInfo   }
            {'model_class':models.Host,'handler':  HostHandler(models.Host,prev)对象中有一个model_class=models.Host   }
        ]
        """
        if not handler_class:
            handler_class = StarkHandler

        self.registration_list.append({
            'model_class': model_class,
            'handler_class': handler_class(self, model_class, prev),
            'prev': prev,
        })

    def get_urlpatterns(self):
        """
        作用： 基于模型类，获取初始化对应模型类的url路由
        :return: urlpatterns列表，
        """
        urlpatterns = []
        for item in self.registration_list:
            model_class = item['model_class']
            handler_class = item['handler_class']
            prev = item['prev']

            # 获取对应模型的所在app名称，和模型类的名称
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name

            # 如果后续不走路由分发。路由设置按照下面方式
            # urlpatterns.append(re_path(r'^%s/%s/add/$' % (app_label, model_name), handler_class.add_view))
            # urlpatterns.append(re_path(r'^%s/%s/delete/(?P<pk>\d+)/$' % (app_label, model_name), handler_class.delete_view))
            # urlpatterns.append(re_path(r'^%s/%s/modify/(?P<pk>\d+)/$' % (app_label, model_name), handler_class.modify_view))
            # urlpatterns.append(re_path(r'^%s/%s/detail/(?P<pk>\d+)/$' % (app_label, model_name), handler_class.detail_view))
            # urlpatterns.append(re_path(r'^%s/%s/list/$' % (app_label, model_name), handler_class.list_view))
            # 如果后续走路由分发，按照下面方式设计
            if prev:
                urlpatterns.append(
                    re_path(r'^%s/%s/%s/' % (app_label, model_name, prev), (handler_class.get_urlpatterns(), None, None))
                )
            else:
                urlpatterns.append(
                    re_path(r'^%s/%s/' % (app_label, model_name), (handler_class.get_urlpatterns(), None, None))
                )

        return urlpatterns

    @property
    def urls(self):
        """
        作用：返回urlpatterns，给setting中路由配置
        :return: 元组
        """
        return self.get_urlpatterns(), self.app_name, self.namespace


# 实例化
stark_site = StarkSite()
