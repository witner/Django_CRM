from django.db import models
# from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserInfo(models.Model):
    """
    用户信息表，通过继承AbstractUser
    一、AbstractUser基本字段
    [username, password]
    1、存放用户的基本信息
    """
    id = models.AutoField(primary_key=True)

    username = models.CharField(verbose_name='用户名', max_length=20, unique=True)

    # 手机号
    telephone = models.CharField(verbose_name='手机号', max_length=20, unique=True)
    # 邮箱
    email = models.CharField(verbose_name='邮箱', max_length=128, unique=True)
    # 密码
    password = models.CharField(verbose_name='密码', max_length=20)
    # 昵称
    nickname = models.CharField(verbose_name='昵称', max_length=16, blank=True, default=u'小白')
    # 性别
    SEX_CHOICES = (
        (u'M', u"男性-Male"),
        (u'F', u"女性-Female"),
    )
    sex = models.CharField(verbose_name="性别", max_length=2, choices=SEX_CHOICES, blank=True, default=u'M')
    # 年龄
    age = models.IntegerField(verbose_name="年龄", blank=True, default=18)
    # 生日
    birthday = models.DateField(verbose_name=u'生日', blank=True, null=True)
    # 地址
    address = models.CharField(verbose_name=u'地址', max_length=128, blank=True, default=u'无')
    # 头像
    avatar = models.FileField(verbose_name='头像', upload_to='avatars/', default='avatars/default.png')

    # 创建时间
    time_create = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    # 用户对应角色
    role = models.ManyToManyField(verbose_name='用户对应角色', to='Role', through='UserToRole',
                                  through_fields=('user', 'role'), blank=True)

    def __str__(self):
        return self.username


class URL(models.Model):
    """
    基于URL的权限
    """
    id = models.AutoField(primary_key=True)
    url = models.CharField(verbose_name='含正则的URL', max_length=256)
    name = models.CharField(verbose_name='URL别名', max_length=128, unique=True)
    comment = models.CharField(verbose_name='备注', null=True, blank=True, max_length=256)
    create_time = models.DateTimeField(verbose_name='创建时间', null=True, auto_now_add=True)
    create_user = models.ForeignKey(verbose_name='创建人', null=True, to='UserInfo', to_field='id',
                                    on_delete=models.CASCADE, related_name='url_create_user')
    update_time = models.DateTimeField(verbose_name='更新时间', null=True, auto_now_add=True)
    update_user = models.ForeignKey(verbose_name='更新人', null=True, to='UserInfo', to_field='id',
                                    on_delete=models.CASCADE, related_name='url_update_user')

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    菜单表
    """
    id = models.AutoField(primary_key=True)
    icon = models.CharField(verbose_name='图标', max_length=32, default='glyphicon glyphicon-tags')
    title = models.CharField(verbose_name='菜单名称', max_length=32)
    TYPE_CHOICES = (
        (1, u"一级导航菜单"),
        (2, u"二级导航菜单"),
        (10, u"普通按钮"),
    )
    type = models.IntegerField(verbose_name='类型', choices=TYPE_CHOICES)
    # 系统状态，0:正常，10:禁用,
    STATE_CHOICES = (
        (0, u"正常"),
        (1, u"禁用"),
    )
    state = models.IntegerField(verbose_name='状态', default=0)
    comment = models.CharField(verbose_name='备注', null=True, blank=True, max_length=256)
    parent_menu = models.ForeignKey(verbose_name='父菜单', to='Menu', to_field='id', null=True, blank=True, default=None,
                                    on_delete=models.CASCADE)
    url = models.OneToOneField(verbose_name='对应URL', to='URL', to_field='id', null=True, blank=True,
                               on_delete=models.CASCADE)
    priority = models.IntegerField(verbose_name='菜单优先级', default=0)
    app_system = models.ForeignKey(verbose_name='菜单所属应用系统', to='AppSystem', to_field='id', null=True, blank=True,
                                   on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间', null=True, auto_now_add=True)
    create_user = models.ForeignKey(verbose_name='创建人', null=True, to='UserInfo', to_field='id',
                                    on_delete=models.CASCADE, related_name='create_user')
    update_time = models.DateTimeField(verbose_name='更新时间', null=True, auto_now_add=True)
    update_user = models.ForeignKey(verbose_name='更新人', null=True, to='UserInfo', to_field='id',
                                    on_delete=models.CASCADE, related_name='update_user')

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='角色名称', max_length=32)
    url_permission = models.ManyToManyField(verbose_name='拥有的URL权限', to='URL', through='RoleToUrlPermission',
                                            through_fields=('role', 'url'), blank=True)
    menu_permission = models.ManyToManyField(verbose_name='拥有的菜单权限', to='Menu', through='RoleToMenuPermission',
                                             through_fields=('role', 'menu'), blank=True)

    def __str__(self):
        return self.title


class RoleToUrlPermission(models.Model):
    """
    角色权限关系表
    """
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(verbose_name='角色', to='Role', to_field='id', on_delete=models.CASCADE)
    url = models.ForeignKey(verbose_name='URL', to='URL', to_field='id', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('role', 'url'),
        ]

    def __str__(self):
        return self.role.title + "---" + self.url.name


class RoleToMenuPermission(models.Model):
    """
    角色权限关系表
    """
    id = models.AutoField(primary_key=True)
    role = models.ForeignKey(verbose_name='角色', to='Role', to_field='id', on_delete=models.CASCADE)
    menu = models.ForeignKey(verbose_name='菜单', to='Menu', to_field='id', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('role', 'menu'),
        ]

    def __str__(self):
        return self.role.title + "---" + self.menu.title


class UserToRole(models.Model):
    """
    用户角色表
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', to_field='id', on_delete=models.CASCADE)
    role = models.ForeignKey(verbose_name='角色', to='Role', to_field='id', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('user', 'role'),
        ]

    def __str__(self):
        return self.user.username + "---" + self.role.title


class AppSystem(models.Model):
    """
    应用系统
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='应用名称', max_length=32)
    comment = models.CharField(verbose_name='应用备注', max_length=256, null=True, blank=True)

    def __str__(self):
        return self.title
