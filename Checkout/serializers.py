from rest_framework import serializers
from .models import Order, OrderHistory
from productmodule.models import Product


class ProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'selling_price']


class OrderSerializer(serializers.ModelSerializer):
    product = ProductBriefSerializer(read_only=True)
    seller_id = serializers.UUIDField(source='product.seller', read_only=True)
    cost_price = serializers.DecimalField(source='product.cost_price', max_digits=10, decimal_places=2, read_only=True)
    total_cost = serializers.SerializerMethodField()


    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'rate', 'total_price','seller_id','cost_price','total_cost']
    def get_total_cost(self, obj):
        try:
            return float(obj.product.cost_price) * obj.quantity
        except:
            return None

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
