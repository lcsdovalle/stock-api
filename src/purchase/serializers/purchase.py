import json

from rest_framework import serializers

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
        ]


class ListPurchaseSerializer(serializers.ModelSerializer):
    customer_info = serializers.SerializerMethodField()
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = [
            "id",
            "customer_info",
            "product_info",
            "origin_order",
            "created_at",
            "owner",
        ]

    def get_customer_info(self, instance_serializer):
        try:
            return json.loads(instance_serializer.customer_info)
        except json.JSONDecodeError:
            return instance_serializer

    def get_product_info(self, instance_serializer):
        try:
            return json.loads(instance_serializer.product_info)
        except json.JSONDecodeError:
            return obj
