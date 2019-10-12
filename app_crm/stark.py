#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 导入系统模块
# 第三方模块

# 导入自定义模块
from .models import *
from app_c_stark.server.stark_site import stark_site

from .views.school import SchoolHandler
from .views.userinfo import UserInfoHandler
from .views.department import DepartmentHandler
from .views.course import CourseHandler
from .views.class_list import ClassListHandler
from .views.public_customer import PublicCustomerHandler
from .views.private_customer import PrivateCustomerHandler

# 设置环境变量

stark_site.register(model_class=School, handler_class=SchoolHandler)
stark_site.register(model_class=Department, handler_class=DepartmentHandler)
stark_site.register(model_class=UserInfo, handler_class=UserInfoHandler)
stark_site.register(model_class=Course, handler_class=CourseHandler)
stark_site.register(model_class=ClassList, handler_class=ClassListHandler)
stark_site.register(model_class=Customer, handler_class=PublicCustomerHandler, prev='pub')
stark_site.register(model_class=Customer, handler_class=PrivateCustomerHandler, prev='pri')
