from django.contrib import admin

from purchase.models.purchase import Purchase
from users.admin import admin_site


class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_info",
        "product_info",
        "origin_order",
        "created_at",
        "updated_at",
        "owner",
    )
    list_display_links = (
        "id",
        "customer_info",
        "product_info",
        "origin_order",
        "created_at",
        "updated_at",
        "owner",
    )
    list_per_page = 25
    ordering = ["-created_at"]


admin_site.register(Purchase, PurchaseAdmin)
# Register your models here.
