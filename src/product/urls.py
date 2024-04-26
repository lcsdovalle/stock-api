from django.urls import path

from product.views.product import ActiveProductListView, ProductCreateView, ProductUpdateView

app_name = "product"  # Add the label for the app

urlpatterns = [
    path("products/active/", ActiveProductListView.as_view(), name="active_products"),
    path("create/", ProductCreateView.as_view(), name="create-product"),
    path("update/<int:pk>/", ProductUpdateView.as_view(), name="update-product"),
]
