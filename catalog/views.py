from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.NumberFilter(field_name="category__id")
    stock_status = django_filters.ChoiceFilter(
        choices=(
            ('in_stock', 'In Stock'),
            ('out_of_stock', 'Out of Stock'),
            ('low_stock', 'Low Stock'),
        ),
        method='filter_stock_status'
    )

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'stock_status']

    def filter_stock_status(self, queryset, name, value):
        if value == 'out_of_stock':
            return queryset.filter(stock_quantity=0)
        elif value == 'low_stock':
            return queryset.filter(stock_quantity__gt=0, stock_quantity__lte=5)
        elif value == 'in_stock':
            return queryset.filter(stock_quantity__gt=5)
        return queryset

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'price', 'stock_quantity', 'created_at']

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        product = self.get_object()
        try:
            adjustment = int(request.data.get('adjustment', 0))
            product.adjust_stock(adjustment)
            return Response({
                'message': 'Stock adjusted successfully',
                'new_stock_quantity': product.stock_quantity
            })
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
