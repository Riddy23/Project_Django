from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', 'description']

    # Filter by category, price range, or stock availability
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        in_stock = self.request.query_params.get('in_stock')

        if category:
            queryset = queryset.filter(category__icontains=category)
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        if in_stock == 'true':
            queryset = queryset.filter(stock__gt=0)

        return queryset

    # Custom action: reduce stock after purchase
    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 1))

        if product.stock >= quantity:
            product.stock -= quantity
            product.save()
            return Response({'message': f'{quantity} item(s) purchased successfully.'})
        else:
            return Response({'error': 'Not enough stock available.'}, status=status.HTTP_400_BAD_REQUEST)

    # Custom action: apply discount
    @action(detail=True, methods=['post'])
    def apply_discount(self, request, pk=None):
        product = self.get_object()
        discount = float(request.data.get('discount_percent', 0))
        product.discount_percent = discount
        product.save()
        return Response({'message': f'Discount of {discount}% applied.'})
      
