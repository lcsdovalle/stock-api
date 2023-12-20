from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.authentication import BearerTokenAuthentication
from product.models.product import Product
from product.serializers.product import ProductSerializer, CreateUpdateProductSerializer


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
        product_id = self.request.query_params.get("id", None)
        name = self.request.query_params.get("name", None)
        description = self.request.query_params.get("description", None)

        if product_id:
            queryset = queryset.filter(id=product_id)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if description:
            queryset = queryset.filter(description__icontains=description)

        return queryset

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateUpdateProductSerializer
