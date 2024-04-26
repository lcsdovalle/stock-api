from decimal import Decimal

from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.authentication import BearerTokenAuthentication
from product.models.product import Product
from product.serializers.product import CreateProductSerializer, ProductSerializer, UpdateProductSerializer
from stock.models.stock import Stock


class ActiveProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerTokenAuthentication]

    def __is_number(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def get_queryset(self):
        """
        This view returns a filtered list of active products based on the
        'id', 'name', and 'description' query parameters.
        """
        queryset = Product.objects.filter(active=True)
        search = self.request.query_params.get("search", None)
        if search:
            if self.__is_number(search):
                queryset = queryset.filter(pk=search)
            else:
                queryset = queryset.filter(
                    Q(name__icontains=search) | Q(description__icontains=search)
                )

        return queryset.order_by("-updated_at")


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer

    def __update_stock(self, product: Product, quantity: int):
        Stock.objects.create(product=product, quantity=quantity)

    def post(self, request, *args, **kwargs):
        try:
            quantity: int = request.data.pop("stock_quantity")
            request.data.pop("id", None)
            request.data.pop("created_at", None)
            request.data["price_sale"] = Decimal(request.data["price_sale"])
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                fresh_product: Product = Product.objects.create(
                    **serializer.validated_data
                )
                self.__update_stock(fresh_product, quantity)

                return Response("Ok", 200)
            return Response("Fail", 400)
        except Exception as e:
            print(e)
            raise e


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = UpdateProductSerializer

    def __get_product_stock(self, product: Product):
        try:
            return Stock.objects.get(product=product)
        except Stock.DoesNotExist:
            return None

    def __create_product_stock(self, product: Product, quantity: int):
        Stock.objects.create(product=product, quantity=quantity)

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        quantity: int = request.data.pop("stock_quantity")
        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            # Update the product stock
            product_stock: Stock = self.__get_product_stock(product)
            if product_stock is not None:
                product_stock.quantity = quantity
                product_stock.save()
            else:
                self.__create_product_stock(product, quantity)

            # Update product data
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
