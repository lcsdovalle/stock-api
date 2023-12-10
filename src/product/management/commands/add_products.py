import random
from decimal import Decimal

from django.core.management.base import BaseCommand

from product.models.product import (
    Product,
)  # Update with the actual path to your Product model


class Command(BaseCommand):
    help = "Adds 5 new products to the database"

    def handle(self, *args, **kwargs):
        terms = ["Essência", "Perfume", "Base", "Aroma"]

        for i in range(5):
            name = f"{random.choice(terms)} {i}"
            price_purchase = Decimal(random.uniform(5.00, 20.00)).quantize(
                Decimal(".01")
            )

            # Convert price_purchase to float for random.uniform function
            price_purchase_float = float(price_purchase)
            price_sale = Decimal(random.uniform(1.00, price_purchase_float)).quantize(
                Decimal(".01")
            )

            product = Product(
                name=name,
                description=f"Description for {name}",
                price_sale=price_sale,
                price_purchase=price_purchase,
                active=True,
            )
            product.save()

        self.stdout.write(self.style.SUCCESS("Successfully added 5 products"))
