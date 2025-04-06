from rest_framework import serializers
from .models import Order, OrderHistory
from productmodule.models import Product


class ProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'selling_price']


class OrderSerializer(serializers.ModelSerializer):
    product = ProductBriefSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'rate', 'total_price']


class OrderHistorySerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)  # Optional: shows username

    class Meta:
        model = OrderHistory
        fields = [
            'id', 'user', 'user_address', 'total_amount',
            'transaction_id', 'payment_id', 'payment_method', 'payment_status',
            'order_status', 'order_date', 'shipping_date', 'delivery_date',
            'orders'
        ]
