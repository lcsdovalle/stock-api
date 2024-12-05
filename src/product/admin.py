from django.contrib import admin

from product.models.product import Product
from users.admin import admin_site


class MyProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_sale", "price_purchase", "active")
    list_editable = ("price_sale", "price_purchase", "active")
    search_fields = ("name", "description")
    list_filter = ("active",)


admin_site.register(Product, MyProductAdmin)
