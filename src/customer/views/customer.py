from django.db.models import Q
from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from customer.models import Customer
from customer.serializers.customer import CustomerSerializer


class CustomerByCPFView(APIView):
    def get(self, request, cpf):
        customer = Customer.objects.filter(cpf=cpf).first()
        if customer:
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        return Response(
            {"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
        )


class CustomerListView(ListAPIView):
    serializer_class = CustomerSerializer
    # Uncomment the line below if you're using a custom pagination class
    # pagination_class = StandardResultsSetPagination

    def get(self, request, *args, **kwargs):
        search = request.query_params.get("search")
        if search:
            customers = Customer.objects.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(cpf__icontains=search)
                | Q(email__icontains=search)
            ).order_by("-created_at")
        else:
            customers = Customer.objects.all().order_by("-created_at")

        # Here we use pagination
        page = self.paginate_queryset(customers)
        if page is None:
            raise Http404("No page found")
        serializer = CustomerSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class CustomerCreateView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Verify if the customer already exists
            cpf = serializer.validated_data.get("cpf")
            customer = Customer.objects.filter(cpf=cpf).first()
            if customer:
                # Update the customer if exists
                serializer = CustomerSerializer(customer, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If not exists, then save.
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
