from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token

TokenAdmin.raw_id_fields = ("user",)


class MyAdminSite(admin.AdminSite):
    site_header = "Sistema de controle de estoque e vendas"
    site_title = "SCEV"
    enable_nav_sidebar = True
    index_title = "Início"
    enable_nav_sidebar = True


admin_site = MyAdminSite(name="myadmin")
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(Token, TokenAdmin)
