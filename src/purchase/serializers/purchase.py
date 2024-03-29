import json

from rest_framework import serializers

from order.serializers.order import OrderSerializer
from purchase.models.purchase import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            "id",
            "customer_info",
            "product_info",
            "origin_order",
            "created_at",
            "updated_at",
            "owner",
            "total_price",
        ]


class ListPurchaseSerializer(serializers.ModelSerializer):
    customer_info = serializers.SerializerMethodField()
    product_info = serializers.SerializerMethodField()
    origin_order = OrderSerializer()

    class Meta:
        model = Purchase
        fields = [
            "id",
            "customer_info",
            "product_info",
            "origin_order",
            "created_at",
            "total_price",
            "owner",
        ]

    def get_customer_info(self, instance_serializer):
        try:
            if customer_info := getattr(instance_serializer, "customer_info", None):
                return json.loads(customer_info)
        except json.JSONDecodeError:
            return instance_serializer

    def get_product_info(self, instance_serializer):
        try:
            if product_info := getattr(instance_serializer, "product_info", None):
                return json.loads(product_info)
        except json.JSONDecodeError:
            return instance_serializer
