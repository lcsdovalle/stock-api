from django.urls import path

from product.views.list import ActiveProductListView

app_name = "product"  # Add the label for the app

urlpatterns = [
    path("products/active/", ActiveProductListView.as_view(), name="active_products"),
]
