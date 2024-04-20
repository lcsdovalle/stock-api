from django.conf import settings
from django.db import models
from django.db.models import JSONField

from order.models.order import (
    Order,
)  # Assuming your order model is in an app named 'order'


class Purchase(models.Model):
    customer_info = JSONField()
    product_info = JSONField()
    origin_order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="purchases"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Purchase {self.id} from Order {self.origin_order.id}"
