from django.urls import path

from order.views.order import CreateOrderView, OrderListView

app_name = "order"  # Add the label for the app

urlpatterns = [
    path("orders", OrderListView.as_view(), name="order_list"),
    path("create-order", CreateOrderView.as_view(), name="create_order"),
]
