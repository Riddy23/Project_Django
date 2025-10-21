from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price',
            'discount_percent', 'discounted_price',
            'category', 'stock', 'created_at'
        ]

    def get_discounted_price(self, obj):
        return obj.discounted_price()
        
