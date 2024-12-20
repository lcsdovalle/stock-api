import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models.order import Order
from order.models.product_order import ProductOrder
from product.models.product import Product
from purchase.models.purchase import Purchase
from purchase.serializers.purchase import PurchaseSerializer
from stock.models.stock import Stock


class TransformOrderToPurchaseView(APIView):
    def __convert_decimal_to_string(self, decimal_value):
        return str(decimal_value)

    def __convert_datetime_to_string(self, datetime_value):
        return datetime_value.strftime("%Y-%m-%d %H:%M:%S")

    def __udpate_stock_upon_purchase(self, product: ProductOrder):
        """Updates the stock quantity upon purchase of a product."""
        stock = self.__get_product_stock(product.product)
        if stock:
            stock.update_quantity(product.quantity)
        else:
            self.__create_product_stock(product.product, product.quantity)

    def __get_product_stock(self, product: Product):
        try:
            return Stock.objects.get(product=product)
        except Stock.DoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None

    def __create_product_stock(self, product: Product, quantity: int):
        Stock.objects.create(product=product, quantity=quantity)

    def __check_if_purchase_exists(self, order_id):
        try:
            return Purchase.objects.get(origin_order=order_id)
        except Purchase.DoesNotExist:
            return None
        except Exception as e:
            print(e)
            return None

    def post(self, request):
        customer_info = {}
        product_info = {}
        order_id = request.data.get("order_id")
        try:
            order: Order = Order.objects.get(id=order_id)
            if self.__check_if_purchase_exists(order_id):
                return Response(
                    {"error": "Purchase already exists"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if customer := getattr(order, "customer", None):
                customer_info = {
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "email": customer.email,
                    "phone": customer.phone,
                    "address": customer.address,
                    "created_at": self.__convert_datetime_to_string(
                        order.customer.created_at
                    ),
                    "updated_at": self.__convert_datetime_to_string(
                        order.customer.updated_at
                    ),
                    "id": order.customer.id,
                }

            product_info = []  # Logic to extract product info from order
            products: list[ProductOrder] = order.productorder_set.all()
            if products:
                for product in products:
                    self.__udpate_stock_upon_purchase(product)
                    product_dict = {
                        "id": product.product.id,
                        "name": product.product.name,
                        "description": product.product.description,
                        "price_sale": self.__convert_decimal_to_string(
                            product.product.price_sale
                        ),
                        "price_purchase": self.__convert_decimal_to_string(
                            product.product.price_purchase
                        ),
                        "quantity": product.quantity,
                        "created_at": self.__convert_datetime_to_string(
                            product.product.created_at
                        ),
                        "updated_at": self.__convert_datetime_to_string(
                            product.product.updated_at
                        ),
                        "active": product.product.active,
                    }
                    product_info.append(product_dict)

            # Order.calculate_total_price(order)
            purchase_data = {
                "customer_info": json.dumps(customer_info) if customer_info else {},
                "product_info": json.dumps(product_info) if product_info else {},
                "origin_order": order.id,
                "owner": request.user.id,  # Current logged-in user
                "total_price": order.total_price,
            }
            serializer = PurchaseSerializer(data=purchase_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
