from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(URL)
admin.site.register(Menu)
admin.site.register(Role)
admin.site.register(RoleToUrlPermission)
admin.site.register(RoleToMenuPermission)
admin.site.register(UserToRole)
admin.site.register(AppSystem)


