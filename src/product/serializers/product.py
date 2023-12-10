from rest_framework import serializers

from product.models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price_sale", "active", "created_at"]

    def to_representation(self, instance):
        return super(ProductSerializer, self).to_representation(instance)
