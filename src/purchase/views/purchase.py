import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models.order import Order
from product.models.product import Product
from purchase.serializers.purchase import PurchaseSerializer


class TransformOrderToPurchaseView(APIView):
    def __convert_decimal_to_string(self, decimal_value):
        return str(decimal_value)

    def __convert_datetime_to_string(self, datetime_value):
        return datetime_value.strftime("%Y-%m-%d %H:%M:%S")

    def post(self, request):
        order_id = request.data.get("order_id")
        try:
            order: Order = Order.objects.get(id=order_id)
            customer_info = {
                "first_name": order.customer.first_name,
                "last_name": order.customer.last_name,
                "email": order.customer.email,
                "phone": order.customer.phone,
                "address": order.customer.address,
                "created_at": self.__convert_datetime_to_string(
                    order.customer.created_at
                ),
                "updated_at": self.__convert_datetime_to_string(
                    order.customer.updated_at
                ),
                "id": order.customer.id,
            }

            product_info = []  # Logic to extract product info from order
            products: list[Product] = order.products.all()
            for product in products:
                product_dict = {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price_sale": self.__convert_decimal_to_string(product.price_sale),
                    "price_purchase": self.__convert_decimal_to_string(
                        product.price_purchase
                    ),
                    "created_at": self.__convert_datetime_to_string(product.created_at),
                    "updated_at": self.__convert_datetime_to_string(product.updated_at),
                    "active": product.active,
                }
                product_info.append(product_dict)

            Order.calculate_total_price(order)
            purchase_data = {
                "customer_info": json.dumps(customer_info),
                "product_info": json.dumps(product_info),
                "origin_order": order.id,
                "owner": request.user.id,  # Current logged-in user
                "total_price": order.total_price,
            }
            serializer = PurchaseSerializer(data=purchase_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
