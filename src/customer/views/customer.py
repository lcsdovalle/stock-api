from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from customer.models import Customer
from customer.serializers.customer import CustomerSerializer

class CustomerByCPFView(APIView):
    def get(self, request, cpf):
        customer = Customer.objects.filter(cpf=cpf).first()
        if customer:
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
