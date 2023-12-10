from django.contrib import admin

from order.models.order import Order
from order.models.product_order import ProductOrder
from users.admin import admin_site


class OrderAdmin(admin.ModelAdmin):
    list_filter = ("owner",)  # Enable filtering by owner
    filter_horizontal = ("products",)  # Enable horizontal filter for products
    filter_vertical = ("products",)  # Enable vertical filter for products
    search_fields = (
        "owner__username",
        "products__name",
        "customer__first_name",
        "customer__last_name",
    )  # Enable search by owner username and product name
    list_display = (
        "id",
        "owner",
        "total_price",
        "discount",
        "customer",
    )  # Display these fields in the admin list
    list_editable = (
        "total_price",
        "owner",
    )  # Enable editing of the discount field in the admin list


class ProductOrderAdmin(admin.ModelAdmin):
    list_filter = ("order",)  # Enable filtering by order
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
    )  # Display these fields in the admin list


admin_site.register(ProductOrder, ProductOrderAdmin)
admin_site.register(Order, OrderAdmin)
