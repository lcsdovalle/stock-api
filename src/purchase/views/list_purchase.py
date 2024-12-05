from django.db.models import Q
from rest_framework import generics

from purchase.models.purchase import Purchase
from purchase.serializers.purchase import ListPurchaseSerializer


class PurchaseListView(generics.ListAPIView):
    serializer_class = ListPurchaseSerializer

    def get_queryset(self):
        """
        Optionally filters the returned purchases based on 'date_from' and 'customer_name'.
        """

        if (
            self.request.user.is_superuser
            or "manager" in self.request.user.groups.values_list("name", flat=True)
        ):
            queryset = Purchase.objects.all()
        else:
            queryset = queryset = Purchase.objects.filter(owner=self.request.user)
        customer_name = self.request.query_params.get("customer_name")
        customer_id = self.request.query_params.get("customer_id")
        month_number = self.request.query_params.get("month_number")
        if month_number:
            # django works with range 1-12 whereas javascript works with 0-11
            number_month: int = int(month_number) + 1
            queryset = queryset.filter(created_at__month=number_month)

        if customer_name:
            queryset = queryset.filter(
                Q(origin_order__customer__first_name__icontains=customer_name)
                | Q(origin_order__customer__last_name__icontains=customer_name)
            )
        if customer_id:
            queryset = queryset.filter(origin_order__customer_id=customer_id)
        return queryset.order_by("-created_at")
