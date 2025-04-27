
from rest_framework import serializers
from .models import CartItem
from productmodule.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class ProductInlineSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "selling_price", "images"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductInlineSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]
