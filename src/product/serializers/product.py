from rest_framework import serializers

from product.models.product import Product
from stock.models.stock import Stock


class ProductSerializer(serializers.ModelSerializer):
    stock_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price_sale",
            "active",
            "created_at",
            "stock_quantity",
        ]

    def to_representation(self, instance):
        return super(ProductSerializer, self).to_representation(instance)

    def get_stock_quantity(self, instance):
        try:
            stock_product = Stock.objects.get(product=instance)
            return stock_product.quantity
        except Exception as e:
            print(e)
            return 0


class CreateUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price_sale", "price_purchase", "active"]
