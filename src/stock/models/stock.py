from django.db import models

from product.models.product import Product


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def update_quantity(self, sold_quantity):
        self.quantity -= sold_quantity
        self.save()

    class Meta:
        app_label = "stock"
