from django.db import models

from api.basemodel import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price_sale = models.DecimalField(max_digits=10, decimal_places=2)
    price_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "product"

    def save(self, *args, **kwargs):
        if self.price_sale is not None:
            self.price_purchase = self.price_sale

        super().save(*args, **kwargs)
