from rest_framework import serializers

from order.models.order import Order
from order.models.product_order import ProductOrder
from product.models.product import Product
from product.serializers.product import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"  # Adjust the fields as needed


class CreateOrderSerializer(serializers.ModelSerializer):
    # Assuming products are provided as a list of product IDs and quantities
    products = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField())
    )

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            product_id = product_data["product"]
            quantity = product_data["quantity"]
            product = Product.objects.get(id=product_id)
            ProductOrder.objects.create(order=order, product=product, quantity=quantity)
        order.refresh_from_db()
        return order

    def to_representation(self, instance: Order):
        representation = {}
        representation["products"] = ProductSerializer(
            instance.products.all(), many=True
        ).data
        representation["id"] = instance.id
        representation["created_at"] = instance.created_at
        representation["owner"] = instance.owner.id
        if instance.customer is not None:
            representation["customer"] = instance.customer.id
        return representation
