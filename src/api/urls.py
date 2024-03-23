from django.urls import include, path

from users.admin import admin_site
from api.settings import API_VERSION


app_name = "api"  # Add the label for the app

urlpatterns = [
    path("admin/", admin_site.urls),
    path(f"{API_VERSION}/users/", include("users.urls")),
    path(f"{API_VERSION}/stock/", include("stock.urls")),
    path(f"{API_VERSION}/product/", include("product.urls")),
    path(f"{API_VERSION}/order/", include("order.urls")),
    path(f"{API_VERSION}/customer/", include("customer.urls")),
    path(f"{API_VERSION}/purchase/", include("purchase.urls")),
]
