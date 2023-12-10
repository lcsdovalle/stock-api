from django.urls import include, path

from users.admin import admin_site

app_name = "api"  # Add the label for the app

urlpatterns = [
    path("admin/", admin_site.urls),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/stock/", include("stock.urls")),
    path("api/v1/product/", include("product.urls")),
    path("api/v1/order/", include("order.urls")),
    path("api/v1/customer/", include("customer.urls")),
    path("api/v1/purchase/", include("purchase.urls")),
]
