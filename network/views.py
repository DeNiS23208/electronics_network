from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer, ProductSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = (
        NetworkNode.objects.select_related("supplier")
        .prefetch_related("products")
        .all()
    )
    serializer_class = NetworkNodeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country"]  # фильтр по стране
    search_fields = ["name", "city", "country", "email"]
    ordering_fields = ["name", "city", "country", "created_at", "debt"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["release_date"]
    search_fields = ["name", "model"]
    ordering_fields = ["release_date", "name", "model"]
