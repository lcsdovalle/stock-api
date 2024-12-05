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


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price_sale", "price_purchase", "active"]


class UpdateProductSerializer(serializers.ModelSerializer):
    stock_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price_sale",
            "price_purchase",
            "active",
            "id",
            "stock_quantity",
        ]
        extra_kwargs = {
            "pk": {"required": True},
            # "name": {"required": False},
            # "description": {"required": False},
            # "price_sale": {"required": False},
            # "price_purchase": {"required": False},
            # "active": {"required": False},
        }

    def get_stock_quantity(self, instance):
        try:
            stock_product = Stock.objects.get(product=instance)
            return stock_product.quantity
        except Stock.DoesNotExist:
            return 0
