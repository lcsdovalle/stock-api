from django.test import TestCase

from product.models.product import Product
from stock.models.stock import Stock


class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(
            name="test", price_purchase=10, price_sale=13
        )

    def test_create_list_product(self):
        Stock.objects.create(product=self.product, quantity=10)
        stocks = Stock.objects.count()
        self.assertGreater(stocks, 0)

    def test_create_stock(self):
        stock = Stock.objects.create(product=self.product, quantity=10)
        self.assertEqual(stock.product.name, "test")

    def test_delete_product(self):
        product = Product.objects.filter(name="test").first()
        product.delete()

        product = Product.objects.filter(name="test")
        self.assertEqual(product.exists(), False)
