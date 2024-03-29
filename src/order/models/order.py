from decimal import Decimal  # Import the Decimal class

from django.conf import settings
from django.db import models

from api.basemodel import BaseModel  # Import the BaseModel class
from customer.models.customer import Customer
from product.models.product import Product  # Import the Product model


class Order(BaseModel):
    # Many-to-many relationship to the Product model
    products = models.ManyToManyField(
        Product, through="order.ProductOrder", related_name="orders"
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders", blank=True, null=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Reference to the user who created the order
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference to the user model
        on_delete=models.CASCADE,
        related_name="orders",
    )

    # Total price of the order
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Percentage of given discounts
    discount = models.FloatField(blank=True, null=True)

    class Meta:
        app_label = "order"  # Explicitly set the app label

    def __str__(self):
        return f"Order {self.id} by {self.owner.username}"

    def calculate_total_price(self):
        """
        Calculate the total price based on the sum of the prices of the products.
        """
        if len(self.productorder_set.all()) == 0:
            self.total_price = 0
            return
        total_price = sum(
            product_order.product.price_sale * product_order.quantity
            for product_order in self.productorder_set.all()
        )
        if self.discount is None:
            self.total_price = total_price
            return
        discount_decimal = Decimal(self.discount) / Decimal(
            100
        )  # Convert float to Decimal
        discount_amount = total_price * discount_decimal
        self.total_price = total_price - discount_amount

    def save(self, *args, **kwargs):
        """
        Overriding the save method to calculate total price before saving.
        """
        if self.pk:
            self.calculate_total_price()
        super(Order, self).save(*args, **kwargs)
