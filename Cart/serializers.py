# cart/serializers.py

from rest_framework import serializers
from .models import CartItem
from productmodule.models import Product

class ProductInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "selling_price", "image_paths"]

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductInlineSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]
