from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.authentication import BearerTokenAuthentication
from product.models.product import Product
from product.serializers.product import CreateUpdateProductSerializer, ProductSerializer
from stock.models.stock import Stock


class ActiveProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]

    def get_queryset(self):
        """
        This view returns a filtered list of active products based on the
        'id', 'name', and 'description' query parameters.
        """
        queryset = Product.objects.filter(active=True)
        search = self.request.query_params.get("search", None)
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(id__icontains=search)
        )

        return queryset


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateUpdateProductSerializer

    def __update_stock(self, product: Product, quantity: int):
        Stock.objects.create(product=product, quantity=quantity)

    def post(self, request, *args, **kwargs):
        quantity: int = request.data.pop("stock_quantity")
        request.data.pop("id", None)
        request.data.pop("created_at", None)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            fresh_product: Product = Product.objects.create(**serializer.validated_data)
            self.__update_stock(fresh_product, quantity)
            return self.create(request, *args, **kwargs)
