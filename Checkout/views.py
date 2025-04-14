import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderHistory
from .serializers import OrderHistorySerializer
from productmodule.models import Product
from Cart.models import Cart, CartItem
import razorpay
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny



class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            cart = Cart.objects.filter(user=user).first()
            if not cart:
                return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            cart_items = CartItem.objects.filter(cart=cart)
            if not cart_items.exists():
                return Response({"error": "No items in cart."}, status=status.HTTP_400_BAD_REQUEST)

            # Extract and validate data
            address = request.data.get("address")
            transaction_id = request.data.get("transaction_id")
            payment_id = request.data.get("payment_id")
            payment_method = request.data.get("payment_method", "").lower()
            payment_status = request.data.get("payment_status", "").lower()

            if not all([address, transaction_id, payment_id, payment_method, payment_status]):
                return Response({"error": "Missing fields in request."}, status=status.HTTP_400_BAD_REQUEST)

            if payment_method not in ['online', 'offline']:
                return Response({"error": "Invalid payment method."}, status=status.HTTP_400_BAD_REQUEST)

            if payment_status not in ['pending', 'success', 'failed']:
                return Response({"error": "Invalid payment status."}, status=status.HTTP_400_BAD_REQUEST)

            order_history_id = str(uuid.uuid4())

            # Calculate total amount from cart
            total_amount = 0
            for cart_item in cart_items:
                total_amount += cart_item.product.selling_price * cart_item.quantity

            # Create OrderHistory
            order_history = OrderHistory.objects.create(
                id=order_history_id,
                user=user,
                user_address=address,
                total_amount=total_amount,
                transaction_id=transaction_id,
                payment_id=payment_id,
                payment_method=payment_method,
                payment_status=payment_status,
                order_status='confirmed'
            )

            # Create individual orders
            for cart_item in cart_items:
                product = cart_item.product
                rate = product.selling_price
                quantity = cart_item.quantity
                total_price = rate * quantity

                Order.objects.create(
                    id=str(uuid.uuid4()),
                    order_history=order_history,
                    product=product,
                    quantity=quantity,
                    rate=rate,
                    total_price=total_price
                )

            # Clear the cart
            cart_items.delete()
            cart.delete()

            serializer = OrderHistorySerializer(order_history)
            return Response({
                "message": "Order placed successfully.",
                "order": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchOrderSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = OrderHistory.objects.filter(user=user).order_by('-order_date')
        serializer = OrderHistorySerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class FetchOrderSummaryView(APIView):
#     permission_classes = [IsAuthenticated]  # Require JWT-authenticated user

#     def get(self, request):
#         user = request.user
#         orders = OrderHistory.objects.filter(user=user).order_by('-order_date')
#         serializer = OrderHistorySerializer(orders, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def razorpayorder(request):
    try:
        amount = int(request.data.get("amount", 0)) * 100  # Razorpay works in paise
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        payment = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        return Response({
            "order_id": payment['id'],
            "amount": payment['amount'],
            "currency": payment['currency'],
            "razorpay_key": settings.RAZORPAY_KEY_ID
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
class FetchAllOrderHistoriesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        orders = OrderHistory.objects.all().order_by('-order_date')
        serializer = OrderHistorySerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Order

@api_view(['POST'])
@permission_classes([AllowAny])
def total_sales_by_seller(request):
    try:
        seller_id = request.data.get('seller_id')
        if not seller_id:
            return Response({'error': 'seller_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter orders where product's seller matches
        seller_orders = Order.objects.filter(product__seller=seller_id)

        # Calculate total sales
        total_sales = seller_orders.aggregate(total=Sum('total_price'))['total'] or 0

        # Annotate each order with calculated profit
        seller_orders = seller_orders.annotate(
            profit=ExpressionWrapper(
                (F('rate') - F('product__cost_price')) * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

        # Sum all profits
        total_profit = seller_orders.aggregate(total=Sum('profit'))['total'] or 0

        return Response({
            'seller_id': seller_id,
            'total_sales': total_sales,
            'total_profit': total_profit
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.db.models import F, Sum, ExpressionWrapper, DecimalField, DateField
from django.db.models.functions import TruncDate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Order

@api_view(['POST'])
@permission_classes([AllowAny])
def total_sales_profit_per_day(request):
    try:
        seller_id = request.data.get('seller_id')
        if not seller_id:
            return Response({'error': 'seller_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter seller orders
        seller_orders = Order.objects.filter(product__seller=seller_id)

        # Annotate each order with profit and truncated date
        seller_orders = seller_orders.annotate(
            order_date=TruncDate('order_history__order_date'),
            profit=ExpressionWrapper(
                (F('rate') - F('product__cost_price')) * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

        # Group by date and aggregate total sales and profit
        daily_summary = seller_orders.values('order_date').annotate(
            total_sales=Sum('total_price'),
            total_profit=Sum('profit')
        ).order_by('order_date')

        return Response(daily_summary, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
