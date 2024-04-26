# isort: skip_file
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from order.models.order import Order
from django.shortcuts import get_object_or_404
from api.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from order.serializers.order import (
    CreateOrderSerializer,
    OrderSerializer,
    OrderUpdateSerializer,
)  # isort: skip

from api.services_helpers.helpers import generate_body_message
from api.services_helpers.printing import save_order_pdf
from django.core.mail import EmailMessage
from django.http import HttpResponse
import os


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
        if (
            self.request.user.is_superuser
            or "manager" in self.request.user.groups.values_list("name", flat=True)
        ):
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(owner=self.request.user)

        number_month = self.request.query_params.get("number_month")
        customer_name = self.request.query_params.get("customer")
        if number_month is not None:
            number_month = int(number_month) + 1
            queryset = queryset.filter(created_at__month=number_month)
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


class SendEmailView(APIView):
    def post(self, request):
        order_id = request.data.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        template = generate_body_message(order_model=order, format="email")
        pdf_path = save_order_pdf(order_id)
        email = EmailMessage(
            subject="Orçamento",
            body=template,
            from_email=EMAIL_HOST_USER,
            to=[order.customer.email],
        )
        email.content_subtype = "html"
        email.attach_file(pdf_path)
        email.send()
        return Response({"message": "Email enviado com sucesso."})


def send_pdf_to_frontend(request):
    order_id = request.GET.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    # Generate PDF
    pdf_path = save_order_pdf(order.id)  # Assumes this method saves the PDF locally

    if not os.path.exists(pdf_path):
        return HttpResponse("Failed to generate PDF.", status=500)

    # Read the PDF file content
    with open(pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()

    # Create a response with the PDF file content
    response = HttpResponse(pdf_data, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="order_{}.pdf"'.format(order_id)
    return response
