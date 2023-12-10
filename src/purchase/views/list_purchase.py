from django.db.models import Q
from django.utils.dateparse import parse_date
from rest_framework import generics

from purchase.models.purchase import Purchase
from purchase.serializers.purchase import ListPurchaseSerializer, PurchaseSerializer


class PurchaseListView(generics.ListAPIView):
    serializer_class = ListPurchaseSerializer

    def get_queryset(self):
        """
        Optionally filters the returned purchases based on 'date_from' and 'customer_name'.
        """
        queryset = Purchase.objects.all()
        date_from = self.request.query_params.get("date_from")
        customer_name = self.request.query_params.get("customer_name")

        if date_from:
            date_from = parse_date(date_from)
            queryset = queryset.filter(created_at__gte=date_from)

        if customer_name:
            # Assuming 'customer_info' contains customer's name
            queryset = queryset.filter(
                Q(origin_order__customer__first_name__icontains=customer_name)
                | Q(origin_order__customer__last_name__icontains=customer_name)
            )

        return queryset
