"""Django_CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from app_c_stark.server.stark_site import stark_site
from app_c_rbac.views import theme_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stark/', stark_site.urls),
    path('app_c_rbac/', include(('app_c_rbac.urls', 'app_c_rbac'))),
    path('index/', theme_views.index),
    # media 路由配置
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^$', theme_views.index),
]
