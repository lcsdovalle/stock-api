# isort: skip_file
from django.utils.dateparse import parse_date
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from order.models.order import Order
from order.serializers.order import (
    CreateOrderSerializer,
    OrderSerializer,
    OrderUpdateSerializer,
)  # isort: skip


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the queryset of orders based on the provided filters.

        :param date_from: The starting date to filter the orders (optional).
        :type date_from: date or str

        :param customer: The name of the customer to filter the orders (optional).
        :type customer: str

        :return: The queryset of orders based on the provided filters.
        :rtype: QuerySet
        """
        queryset = Order.objects.all()
        date_from = self.request.query_params.get("date_from")
        customer_name = self.request.query_params.get("customer")
        if date_from is not None:
            date = parse_date(date_from)
            queryset = queryset.filter(
                created_at__date__gte=date, created_at__date__lte=date.today()
            )
        if customer_name is not None:
            queryset = queryset.filter(customer__first_name__icontains=customer_name)

        return queryset.order_by("-created_at")


class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer


class AddProductToOrderView(generics.UpdateAPIView):
    serializer_class = OrderUpdateSerializer

    def get_object(self):
        order_id = self.kwargs.get("order_id")
        return Order.objects.get(id=order_id)

    def perform_update(self, serializer):
        serializer.add_product(self.get_object(), serializer.validated_data)


class RemoveProductFromOrderView(generics.UpdateAPIView):
    serializer_class = OrderUpdateSerializer

    def get_object(self):
        order_id = self.kwargs.get("order_id")
        return Order.objects.get(id=order_id)

    def perform_update(self, serializer):
        serializer.remove_product(self.get_object(), serializer.validated_data)
