# Generated by Django 2.2.5 on 2019-09-12 20:03

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('telephone', models.CharField(max_length=20, unique=True, verbose_name='手机号')),
                ('email', models.CharField(max_length=128, unique=True, verbose_name='邮箱')),
                ('nickname', models.CharField(blank=True, default='小白', max_length=16, verbose_name='昵称')),
                ('sex', models.CharField(blank=True, choices=[('M', '男性-Male'), ('F', '女性-Female')], default='M', max_length=2, verbose_name='性别')),
                ('age', models.IntegerField(blank=True, default=18, verbose_name='年龄')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('address', models.CharField(blank=True, default='无', max_length=128, verbose_name='地址')),
                ('avatar', models.FileField(default='avatars/default.png', upload_to='avatars/', verbose_name='头像')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AppSystem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='应用名称')),
                ('comment', models.CharField(blank=True, max_length=256, null=True, verbose_name='应用备注')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('icon', models.CharField(default='glyphicon glyphicon-tags', max_length=32, verbose_name='图标')),
                ('title', models.CharField(max_length=32, verbose_name='菜单名称')),
                ('type', models.IntegerField(choices=[(1, '一级导航菜单'), (2, '二级导航菜单'), (10, '普通按钮')], verbose_name='类型')),
                ('state', models.IntegerField(default=0, verbose_name='状态')),
                ('comment', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('priority', models.IntegerField(default=0, verbose_name='菜单优先级')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='更新时间')),
                ('app_system', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_c_rbac.AppSystem', verbose_name='菜单所属应用系统')),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='create_user', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('parent_menu', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_c_rbac.Menu', verbose_name='父菜单')),
                ('update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='update_user', to=settings.AUTH_USER_MODEL, verbose_name='更新人')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='角色名称')),
            ],
        ),
        migrations.CreateModel(
            name='UserToRole',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_c_rbac.Role', verbose_name='角色')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'unique_together': {('user', 'role')},
            },
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=256, verbose_name='含正则的URL')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='URL别名')),
                ('comment', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='更新时间')),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='url_create_user', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='url_update_user', to=settings.AUTH_USER_MODEL, verbose_name='更新人')),
            ],
        ),
        migrations.CreateModel(
            name='RoleToUrlPermission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_c_rbac.Role', verbose_name='角色')),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_c_rbac.URL', verbose_name='URL')),
            ],
            options={
                'unique_together': {('role', 'url')},
            },
        ),
        migrations.CreateModel(
            name='RoleToMenuPermission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_c_rbac.Menu', verbose_name='菜单')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_c_rbac.Role', verbose_name='角色')),
            ],
            options={
                'unique_together': {('role', 'menu')},
            },
        ),
        migrations.AddField(
            model_name='role',
            name='menu_permission',
            field=models.ManyToManyField(blank=True, through='app_c_rbac.RoleToMenuPermission', to='app_c_rbac.Menu', verbose_name='拥有的菜单权限'),
        ),
        migrations.AddField(
            model_name='role',
            name='url_permission',
            field=models.ManyToManyField(blank=True, through='app_c_rbac.RoleToUrlPermission', to='app_c_rbac.URL', verbose_name='拥有的URL权限'),
        ),
        migrations.AddField(
            model_name='menu',
            name='url',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_c_rbac.URL', verbose_name='对应URL'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='role',
            field=models.ManyToManyField(blank=True, through='app_c_rbac.UserToRole', to='app_c_rbac.Role', verbose_name='用户对应角色'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
