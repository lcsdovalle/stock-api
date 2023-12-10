from django.urls import path

from purchase.views.list_purchase import PurchaseListView
from purchase.views.purchase import TransformOrderToPurchaseView

urlpatterns = [
    path(
        "register-purchase",
        TransformOrderToPurchaseView.as_view(),
        name="transform_order_to_purchase",
    ),
    path("list", PurchaseListView.as_view(), name="purchase_list"),
]
