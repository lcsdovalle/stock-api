from django.urls import path

from order.views.order import (  # isort: skip
    AddProductToOrderView,
    CreateOrderView,
    OrderListView,
    RemoveProductFromOrderView,
    SendEmailView,
    send_pdf_to_frontend,
)

app_name = "order"  # Add the label for the app

urlpatterns = [
    path("orders", OrderListView.as_view(), name="order-list"),
    path("create-order", CreateOrderView.as_view(), name="create_order"),
    path(
        "<int:order_id>/add-product",
        AddProductToOrderView.as_view(),
        name="add-product-to-order",
    ),
    path(
        "<int:order_id>/remove-product",
        RemoveProductFromOrderView.as_view(),
        name="remove-product-from-order",
    ),
    path(
        "send-email",
        SendEmailView.as_view(),
        name="send-email",
    ),
    path(
        "print-order/",
        send_pdf_to_frontend,
        name="print-order",
    ),
]
