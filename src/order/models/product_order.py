from django.db import models

from order.models.order import Order
from product.models.product import Product


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        app_label = "order"
        unique_together = (
            "product",
            "order",
        )  # Ensure each product appears only once per order
